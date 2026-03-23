import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd

st.set_page_config(page_title="ניהול ספרים", layout="centered")

st.title("📚 מאגר הספרים שלי (מחובר לגוגל)")

# קישור לגיליון שלך
spreadsheet_url = "https://docs.google.com/spreadsheets/d/1o6yjdU8yo3vNWXFGLqYVCyR_bSYFif_6csZNRvrWJ34/edit?usp=sharing"

# יצירת החיבור
conn = st.connection("gsheets", type=GSheetsConnection)

# קריאת הנתונים בצורה בטוחה
try:
    # קורא את כל הגיליון
    df = conn.read(spreadsheet=spreadsheet_url)
    # אם הגיליון ריק או לא קיים, יוצר מבנה בסיסי
    if df is None or df.empty:
        df = pd.DataFrame(columns=["שם הספר", "מיקום"])
except Exception:
    # במקרה של שגיאה בקריאה (למשל גיליון ריק לגמרי)
    df = pd.DataFrame(columns=["שם הספר", "מיקום"])

# ניקוי שורות ריקות
df = df.dropna(how="all")

# תפריט צד להוספה
st.sidebar.header("הוספת ספר חדש")
book_name = st.sidebar.text_input("שם הספר")
book_location = st.sidebar.text_input("מיקום הספר")

if st.sidebar.button("שמור במאגר"):
    if book_name and book_location:
        # יצירת שורה חדשה
        new_row = pd.DataFrame([{"שם הספר": book_name, "מיקום": book_location}])
        
        # חיבור הנתונים החדשים לישנים
        if df.empty:
            updated_df = new_row
        else:
            updated_df = pd.concat([df, new_row], ignore_index=True)
        
        # עדכון הגליון בגוגל
        conn.update(spreadsheet=spreadsheet_url, data=updated_df)
        st.sidebar.success(f"הספר '{book_name}' נשמר!")
        st.rerun()
    else:
        st.sidebar.error("נא למלא את שני השדות")

# חיפוש
st.header("🔍 חיפוש ספר")
search_query = st.text_input("הקלידי שם לחיפוש:")

if search_query:
    # חיפוש חכם שמתעלם מאותיות גדולות/קטנות
    results = df[df["שם הספר"].astype(str).str.contains(search_query, case=False, na=False)]
    if not results.empty:
        st.table(results)
    else:
        st.warning("הספר לא נמצא במאגר")
else:
    st.write("כל הספרים במאגר:")
    if not df.empty:
        st.dataframe(df, use_container_width=True)
    else:
        st.info("המאגר ריק כרגע. הוסיפי ספר בתפריט הצד!")
