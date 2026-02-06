"""
Odds Comparator Module
Compares odds between two different bookmakers
"""
from typing import Dict, List, Optional
from api_client import APIFootballClient


class OddsComparator:
    """Compares odds between two bookmakers"""
    
    def __init__(self, api_client: APIFootballClient):
        """
        Initialize the comparator
        
        Args:
            api_client: APIFootballClient instance
        """
        self.api_client = api_client
    
    def get_bookmaker_odds(self, odds_data: Dict, bookmaker_id: int) -> Optional[Dict]:
        """
        Extract odds for a specific bookmaker from the API response
        
        Args:
            odds_data: Full odds data from API
            bookmaker_id: ID of the bookmaker to extract
            
        Returns:
            Dictionary with bookmaker odds or None if not found
        """
        if not odds_data.get('response') or len(odds_data['response']) == 0:
            print(f"[DEBUG] No response in odds_data")
            return None
        
        response = odds_data['response'][0]
        bookmakers = response.get('bookmakers', [])
        
        print(f"[DEBUG] Looking for bookmaker ID: {bookmaker_id}")
        print(f"[DEBUG] Found {len(bookmakers)} bookmakers in response")
        print(f"[DEBUG] Available bookmaker IDs: {[bm.get('id') for bm in bookmakers]}")
        
        # Try to find by ID (as integer)
        for bookmaker in bookmakers:
            bm_id = bookmaker.get('id')
            print(f"[DEBUG] Checking bookmaker ID: {bm_id} (type: {type(bm_id)}) vs looking for: {bookmaker_id} (type: {type(bookmaker_id)})")
            if bm_id == bookmaker_id:
                print(f"[DEBUG] Found bookmaker: {bookmaker.get('name')}")
                return {
                    'id': bookmaker.get('id'),
                    'name': bookmaker.get('name'),
                    'bets': bookmaker.get('bets', [])
                }
        
        # Try to find by ID (as string, in case API returns it as string)
        bookmaker_id_str = str(bookmaker_id)
        for bookmaker in bookmakers:
            bm_id = str(bookmaker.get('id'))
            if bm_id == bookmaker_id_str:
                print(f"[DEBUG] Found bookmaker (as string): {bookmaker.get('name')}")
                return {
                    'id': bookmaker.get('id'),
                    'name': bookmaker.get('name'),
                    'bets': bookmaker.get('bets', [])
                }
        
        print(f"[DEBUG] Bookmaker {bookmaker_id} not found")
        return None
    
    def compare_odds(self, fixture_id: int, bookmaker1_id: int, bookmaker2_id: int) -> Dict:
        """
        Compare odds between two bookmakers for a specific fixture
        
        Args:
            fixture_id: The fixture ID
            bookmaker1_id: ID of first bookmaker
            bookmaker2_id: ID of second bookmaker
            
        Returns:
            Dictionary containing comparison results
        """
        # Get odds data from API
        print(f"[DEBUG] Getting odds for fixture_id: {fixture_id}")
        odds_data = self.api_client.get_odds(fixture_id)
        
        print(f"[DEBUG] Odds data keys: {odds_data.keys() if isinstance(odds_data, dict) else 'Not a dict'}")
        if isinstance(odds_data, dict) and 'response' in odds_data:
            print(f"[DEBUG] Response length: {len(odds_data.get('response', []))}")
        
        if not odds_data.get('response') or len(odds_data['response']) == 0:
            return {
                'error': 'No odds data found for this fixture',
                'fixture_id': fixture_id
            }
        
        response = odds_data['response'][0]
        fixture_info = response.get('fixture', {})
        league_info = response.get('league', {})
        
        print(f"[DEBUG] Fixture info: {fixture_info.get('id') if fixture_info else 'None'}")
        print(f"[DEBUG] League info: {league_info.get('name') if league_info else 'None'}")
        
        # Extract odds for both bookmakers
        bookmaker1 = self.get_bookmaker_odds(odds_data, bookmaker1_id)
        bookmaker2 = self.get_bookmaker_odds(odds_data, bookmaker2_id)
        
        if not bookmaker1:
            return {
                'error': f'Bookmaker {bookmaker1_id} not found for this fixture',
                'fixture_id': fixture_id
            }
        
        if not bookmaker2:
            return {
                'error': f'Bookmaker {bookmaker2_id} not found for this fixture',
                'fixture_id': fixture_id
            }
        
        # Compare odds
        comparison = self._compare_bookmaker_odds(bookmaker1, bookmaker2)
        
        return {
            'fixture_id': fixture_id,
            'fixture': fixture_info,
            'league': league_info,
            'bookmaker1': {
                'id': bookmaker1['id'],
                'name': bookmaker1['name']
            },
            'bookmaker2': {
                'id': bookmaker2['id'],
                'name': bookmaker2['name']
            },
            'comparisons': comparison
        }
    
    def _compare_bookmaker_odds(self, bookmaker1: Dict, bookmaker2: Dict) -> List[Dict]:
        """
        Compare odds between two bookmakers
        
        Args:
            bookmaker1: First bookmaker data
            bookmaker2: Second bookmaker data
            
        Returns:
            List of comparison results for each bet type
        """
        comparisons = []
        
        # Create a map of bet types for quick lookup - normalize IDs to int
        def normalize_id(bet_id):
            """Convert bet ID to int if possible"""
            try:
                return int(bet_id)
            except (ValueError, TypeError):
                return bet_id
        
        bets1_map = {normalize_id(bet['id']): bet for bet in bookmaker1.get('bets', [])}
        bets2_map = {normalize_id(bet['id']): bet for bet in bookmaker2.get('bets', [])}
        
        # Get all unique bet IDs
        all_bet_ids = set(bets1_map.keys()) | set(bets2_map.keys())
        
        # Sort bet IDs - try as ints first, then as strings
        try:
            sorted_bet_ids = sorted(all_bet_ids, key=lambda x: (0, x) if isinstance(x, (int, float)) else (1, str(x)))
        except Exception:
            sorted_bet_ids = sorted(all_bet_ids, key=str)
        
        # Bet types to exclude from comparison
        EXCLUDED_BET_NAMES = {
            "HT/FT Double",
            "Exact Score",
            "Odd/Even",
            "Correct Score - First Half",
        }
        
        for bet_id in sorted_bet_ids:
            bet1 = bets1_map.get(bet_id)
            bet2 = bets2_map.get(bet_id)
            
            if not bet1 or not bet2:
                continue  # Skip if one bookmaker doesn't have this bet type
            
            bet_name = bet1.get('name', bet2.get('name', f'Bet {bet_id}'))
            
            # Skip excluded bet types (by exact name)
            if bet_name in EXCLUDED_BET_NAMES:
                continue

            # If one of the bookmakers has 3-way style values (e.g. Over/Under/Exactly),
            # היחסים כבר לא ברי השוואה בצורה פשוטה -> מדלגים על כל המרקט הזה.
            def has_exactly_value(bet: Dict) -> bool:
                for v in bet.get('values', []):
                    val = v.get('value')
                    if isinstance(val, str) and val.strip().lower().startswith("exactly"):
                        return True
                return False
            
            if has_exactly_value(bet1) or has_exactly_value(bet2):
                continue
            
            # Compare values within this bet type
            values1_map = {v['value']: float(v['odd']) for v in bet1.get('values', [])}
            values2_map = {v['value']: float(v['odd']) for v in bet2.get('values', [])}
            
            all_values = set(values1_map.keys()) | set(values2_map.keys())
            
            value_comparisons = []
            # Sort values - try to convert to numbers if possible, otherwise sort as strings
            try:
                # Try to convert values to numbers for sorting
                def sort_key(val):
                    if isinstance(val, (int, float)):
                        return (0, val)  # Numbers first
                    try:
                        return (0, float(val))  # Try to convert string to float
                    except (ValueError, TypeError):
                        return (1, str(val))  # Strings last
                sorted_values = sorted(all_values, key=sort_key)
            except Exception:
                # Fallback: sort as strings
                sorted_values = sorted(all_values, key=str)
            
            for value in sorted_values:
                odd1 = values1_map.get(value)
                odd2 = values2_map.get(value)
                
                if odd1 is None or odd2 is None:
                    continue
                
                # Calculate difference and percentage difference
                diff = odd2 - odd1
                percent_diff = (diff / odd1) * 100 if odd1 > 0 else 0
                
                # Determine which is better (higher odd is better for bettors)
                better = None
                if odd1 > odd2:
                    better = 'bookmaker1'
                elif odd2 > odd1:
                    better = 'bookmaker2'
                else:
                    better = 'equal'
                
                # Show only rows where Bet365 (bookmaker2) is better
                # and the percent difference is at least 2%
                if better == 'bookmaker2' and percent_diff >= 2:
                    value_comparisons.append({
                        'value': value,
                        'bookmaker1_odd': odd1,
                        'bookmaker2_odd': odd2,
                        'difference': round(diff, 3),
                        'percent_difference': round(percent_diff, 2),
                        'better': better
                    })
            
            if value_comparisons:
                comparisons.append({
                    'bet_id': bet_id,
                    'bet_name': bet_name,
                    'values': value_comparisons
                })
        
        return comparisons
