import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd

st.set_page_config(page_title="ניהול ספרים", layout="centered")

st.title("📚 שבת אחת וסיימתם")

# קישור לגיליון שלך
spreadsheet_url = "https://docs.google.com/spreadsheets/d/1o6yjdU8yo3vNWXFGLqYVCyR_bSYFif_6csZNRvrWJ34/edit?usp=sharing"

conn = st.connection("gsheets", type=GSheetsConnection)

# קריאת הנתונים
try:
    df = conn.read(spreadsheet=spreadsheet_url)
    if df is None or df.empty:
        df = pd.DataFrame(columns=["שם הספר", "שם המחבר", "מיקום"])
except Exception:
    df = pd.DataFrame(columns=["שם הספר", "שם המחבר", "מיקום"])

df = df.dropna(how="all")

# תפריט צד להוספה
st.sidebar.header("הוספת ספר חדש")
book_name = st.sidebar.text_input("שם הספר")
author_name = st.sidebar.text_input("שם המחבר") # שדה חדש
book_location = st.sidebar.text_input("מיקום הספר")

if st.sidebar.button("שמור במאגר"):
    if book_name and author_name and book_location:
        new_row = pd.DataFrame([{"שם הספר": book_name, "שם המחבר": author_name, "מיקום": book_location}])
        updated_df = pd.concat([df, new_row], ignore_index=True)
        
        conn.update(spreadsheet=spreadsheet_url, data=updated_df)
        st.sidebar.success(f"הספר '{book_name}' נשמר!")
        st.rerun()
    else:
        st.sidebar.error("נא למלא את כל השדות")

# חיפוש
st.header("🔍 חיפוש ספר")
search_query = st.text_input("חפשי לפי שם ספר או מחבר:")

if search_query:
    # חיפוש שבודק גם בשם הספר וגם בשם המחבר
    mask = (df["שם הספר"].astype(str).str.contains(search_query, case=False, na=False)) | \
           (df["שם המחבר"].astype(str).str.contains(search_query, case=False, na=False))
    results = df[mask]
    
    if not results.empty:
        st.table(results)
    else:
        st.warning("לא נמצאו תוצאות")
else:
    st.write("כל הספרים במאגר:")
    st.dataframe(df, use_container_width=True)
