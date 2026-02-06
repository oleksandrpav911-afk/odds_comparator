# הוראות דיפלוי ל-Render

## שלב 1: הכנת GitHub Repository

1. **צור repository חדש ב-GitHub:**
   - לך ל-https://github.com/new
   - שם: `odds-comparator` (או כל שם שתרצה)
   - בחר Public או Private
   - **אל תסמן** "Add README" או "Add .gitignore" (כי כבר יש לך)

2. **העלה את הקוד ל-GitHub:**
   
   פתח PowerShell בתיקיית הפרויקט (`C:\Users\elisa\odds_comparator`) והרץ:

   ```powershell
   # אם עדיין לא עשית git init
   git init
   
   # הוסף את כל הקבצים
   git add .
   
   # צור commit ראשון
   git commit -m "Initial commit - Odds Comparator"
   
   # הוסף את ה-remote (החלף USERNAME ו-REPO_NAME בשם שלך)
   git remote add origin https://github.com/USERNAME/REPO_NAME.git
   
   # העלה ל-GitHub
   git branch -M main
   git push -u origin main
   ```

   **חשוב:** אם GitHub מבקש ממך username/password, תצטרך להשתמש ב-Personal Access Token במקום סיסמה.

---

## שלב 2: הגדרת Render

1. **הירשם ל-Render:**
   - לך ל-https://render.com
   - הירשם עם GitHub (הכי קל)

2. **צור Web Service חדש:**
   - לחץ על **"New +"** → **"Web Service"**
   - בחר את ה-repository שיצרת ב-GitHub
   - לחץ **"Connect"**

3. **הגדר את השירות:**
   - **Name:** `odds-comparator` (או כל שם)
   - **Region:** בחר הכי קרוב אליך
   - **Branch:** `main`
   - **Root Directory:** (השאר ריק)
   - **Runtime:** `Python 3`
   - **Build Command:** 
     ```
     pip install -r requirements.txt
     ```
   - **Start Command:**
     ```
     gunicorn app:app
     ```
   - **Plan:** בחר **Free** (או Starter אם תרצה)

4. **הוסף Environment Variable:**
   - גלול למטה ל-**"Environment Variables"**
   - לחץ **"Add Environment Variable"**
   - **Key:** `API_FOOTBALL_KEY`
   - **Value:** `5ad413f22d6acfcf65878397513381f6` (המפתח שלך)
   - לחץ **"Save Changes"**

5. **Deploy:**
   - לחץ **"Create Web Service"**
   - Render יתחיל לבנות ולהעלות את האפליקציה (זה יכול לקחת 2-5 דקות)

6. **קבל את ה-URL:**
   - אחרי שהדיפלוי מסתיים, תקבל URL כמו:
     ```
     https://odds-comparator.onrender.com
     ```
   - זה הכתובת הקבועה שלך! שלח אותה לחבר שלך.

---

## שלב 3: עדכון האתר (כל פעם שאתה עושה שינויים)

**זה פשוט מאוד!** כל פעם שאתה עושה שינויים בקוד:

1. **עדכן את הקוד ב-GitHub:**
   ```powershell
   # בתיקיית הפרויקט
   git add .
   git commit -m "תיאור השינויים שעשית"
   git push
   ```

2. **Render יעדכן אוטומטית:**
   - Render מזהה ש-push חדש ב-GitHub
   - הוא מתחיל build חדש אוטומטית
   - אחרי 2-5 דקות האתר מעודכן!

**זה הכל!** אין צורך לעשות משהו ב-Render - זה קורה אוטומטית.

---

## פתרון בעיות

### אם הדיפלוי נכשל:
- בדוק את ה-Logs ב-Render (יש כפתור "Logs" בדף השירות)
- ודא ש-`requirements.txt` מעודכן
- ודא ש-`Procfile` קיים ונכון

### אם האתר לא עובד:
- בדוק שה-Environment Variable `API_FOOTBALL_KEY` מוגדר נכון
- בדוק את ה-Logs ב-Render

### אם אתה רוצה לראות את ה-Logs בזמן אמת:
- לך לדף השירות ב-Render
- לחץ על **"Logs"** - תראה את כל הפלט של האפליקציה

---

## הערות חשובות:

1. **Free Plan של Render:**
   - האתר "נרדם" אחרי 15 דקות של חוסר שימוש
   - הפעלה ראשונה אחרי שינה לוקחת 30-60 שניות
   - זה בסדר גמור לשימוש אישי!

2. **אבטחה:**
   - ה-`.env` לא נשלח ל-GitHub (כי הוא ב-`.gitignore`)
   - המפתח API מוגדר ב-Render ולא בקוד
   - זה בטוח!

3. **עדכונים:**
   - כל `git push` מעדכן את האתר אוטומטית
   - אין צורך לעשות משהו ב-Render

---

**בהצלחה! 🚀**
