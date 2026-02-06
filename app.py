"""
Flask Web Application for Odds Comparison
"""
from flask import Flask, render_template, request, jsonify
from api_client import APIFootballClient
from odds_comparator import OddsComparator
import os
from dotenv import load_dotenv

# Load environment variables from .env file
from pathlib import Path
env_path = Path('.') / '.env'
load_dotenv(dotenv_path=env_path)
print(f"[DEBUG] Loading .env from: {env_path.absolute()}")
print(f"[DEBUG] .env exists: {env_path.exists()}")

app = Flask(__name__)

# Initialize API client and comparator
try:
    print("[DEBUG] Initializing API client...")
    api_key = os.getenv('API_FOOTBALL_KEY')
    print(f"[DEBUG] API key from env: {api_key[:10] if api_key else 'None'}...")
    api_client = APIFootballClient()
    print("[DEBUG] API client initialized successfully")
    comparator = OddsComparator(api_client)
    print("[DEBUG] Comparator initialized successfully")
except ValueError as e:
    print(f"[ERROR] Warning: {e}")
    api_client = None
    comparator = None
except Exception as e:
    print(f"[ERROR] Failed to initialize: {e}")
    api_client = None
    comparator = None


@app.route('/')
def index():
    """Main page"""
    return render_template('index.html')


@app.route('/api/compare', methods=['POST'])
def compare_odds():
    """API endpoint to compare odds between two bookmakers"""
    if not comparator:
        return jsonify({'error': 'API client not initialized. Please set API_FOOTBALL_KEY environment variable'}), 500
    
    data = request.get_json()
    
    fixture_id = data.get('fixture_id')
    bookmaker1_id = data.get('bookmaker1_id')
    bookmaker2_id = data.get('bookmaker2_id')
    
    if not all([fixture_id, bookmaker1_id, bookmaker2_id]):
        return jsonify({'error': 'Missing required parameters: fixture_id, bookmaker1_id, bookmaker2_id'}), 400
    
    try:
        fixture_id = int(fixture_id)
        bookmaker1_id = int(bookmaker1_id)
        bookmaker2_id = int(bookmaker2_id)
    except ValueError:
        return jsonify({'error': 'Invalid parameter types. All IDs must be integers'}), 400
    
    try:
        result = comparator.compare_odds(fixture_id, bookmaker1_id, bookmaker2_id)
        
        if 'error' in result:
            return jsonify(result), 404
        
        return jsonify(result)
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/bookmakers', methods=['GET'])
def get_bookmakers():
    """Get list of available bookmakers"""
    print("[DEBUG] /api/bookmakers called")
    if not api_client:
        print("[ERROR] API client is None!")
        return jsonify({'error': 'API client not initialized'}), 500
    
    try:
        print("[DEBUG] Calling api_client.get_bookmakers()")
        result = api_client.get_bookmakers()
        print(f"[DEBUG] Got result: {type(result)}")
        return jsonify(result)
    except Exception as e:
        print(f"[ERROR] Exception in get_bookmakers: {e}")
        return jsonify({'error': str(e)}), 500


@app.route('/api/fixtures', methods=['GET'])
def get_fixtures():
    """Get fixtures for a specific date"""
    print("[DEBUG] /api/fixtures called")
    if not api_client:
        print("[ERROR] API client is None!")
        return jsonify({'error': 'API client not initialized'}), 500
    
    date = request.args.get('date')
    league = request.args.get('league')
    season = request.args.get('season')
    print(f"[DEBUG] Params: date={date}, league={league}, season={season}")
    
    try:
        league_id = int(league) if league else None
        season_year = int(season) if season else None
        print(f"[DEBUG] Calling api_client.get_fixtures(date={date}, league={league_id}, season={season_year})")
        result = api_client.get_fixtures(date=date, league=league_id, season=season_year)
        print(f"[DEBUG] Got result: {type(result)}")
        return jsonify(result)
    except ValueError as e:
        print(f"[ERROR] ValueError: {e}")
        return jsonify({'error': 'Invalid league ID or season'}), 400
    except Exception as e:
        print(f"[ERROR] Exception in get_fixtures: {e}")
        return jsonify({'error': str(e)}), 500


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(debug=False, host='0.0.0.0', port=port)
