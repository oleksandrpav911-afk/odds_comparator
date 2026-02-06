# השוואת יחסי הימורים - Odds Comparator

אפליקציית ווב להשוואת יחסי הימורים בין שני ספקי הימורים שונים באמצעות API-Football.

## תכונות

- השוואת יחסי הימורים בין שני bookmakers שונים
- ממשק ווב נוח ויפה
- תצוגה מפורטת של ההבדלים בין הספקים
- זיהוי אוטומטי של הספק עם היחס הטוב יותר

## התקנה

1. התקן את התלויות:
```bash
pip install -r requirements.txt
```

2. הגדר את מפתח ה-API:
```bash
# Windows PowerShell
$env:API_FOOTBALL_KEY="your_api_key_here"

# Windows CMD
set API_FOOTBALL_KEY=your_api_key_here

# Linux/Mac
export API_FOOTBALL_KEY=your_api_key_here
```

או צור קובץ `.env` (לא נכלל ב-git):
```
API_FOOTBALL_KEY=your_api_key_here
```

## שימוש

1. הפעל את האפליקציה:
```bash
python app.py
```

2. פתח דפדפן וגש ל:
```
http://localhost:5000
```

3. הזן:
   - **Fixture ID**: מספר המשחק (לדוגמה: 1391043)
   - **Bookmaker 1 ID**: מספר הספק הראשון (לדוגמה: 1)
   - **Bookmaker 2 ID**: מספר הספק השני (לדוגמה: 8)

4. לחץ על "השווה יחסי הימורים"

## API Endpoints

### POST /api/compare
השווה יחסי הימורים בין שני bookmakers

**Request Body:**
```json
{
  "fixture_id": 1391043,
  "bookmaker1_id": 1,
  "bookmaker2_id": 8
}
```

**Response:**
```json
{
  "fixture_id": 1391043,
  "fixture": {...},
  "league": {...},
  "bookmaker1": {
    "id": 1,
    "name": "10Bet"
  },
  "bookmaker2": {
    "id": 8,
    "name": "Bet365"
  },
  "comparisons": [...]
}
```

### GET /api/bookmakers
קבל רשימה של כל ה-bookmakers הזמינים

### GET /api/fixtures
קבל רשימת משחקים

**Query Parameters:**
- `date`: תאריך בפורמט YYYY-MM-DD (אופציונלי)
- `league`: מספר ליגה (אופציונלי)

## מבנה הפרויקט

```
odds_comparator/
├── api_client.py          # לקוח API-Football
├── odds_comparator.py     # לוגיקת השוואת היחסים
├── app.py                 # אפליקציית Flask
├── templates/
│   └── index.html         # ממשק המשתמש
├── requirements.txt       # תלויות Python
└── README.md             # קובץ זה
```

## דוגמאות לשימוש

### דוגמה 1: השוואה בסיסית
```python
from api_client import APIFootballClient
from odds_comparator import OddsComparator

# אתחול
client = APIFootballClient(api_key="your_key")
comparator = OddsComparator(client)

# השוואה
result = comparator.compare_odds(
    fixture_id=1391043,
    bookmaker1_id=1,  # 10Bet
    bookmaker2_id=8   # Bet365
)

print(result)
```

## הערות

- ודא שיש לך מנוי פעיל ל-API-Football
- חלק מהמשחקים עשויים לא לכלול את כל ה-bookmakers
- ה-API מוגבל לפי תוכנית המנוי שלך

## רישיון

פרויקט זה הוא לשימוש אישי.
