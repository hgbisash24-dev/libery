import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd

st.set_page_config(page_title="ניהול ספרים", layout="centered")

st.title("📚 מאגר הספרים שלי (מחובר לגוגל)")

# חיבור לגוגל שיטס
# החליפי את הקישור למטה בקישור של הגיליון שלך!
spreadsheet_url = "https://docs.google.com/spreadsheets/d/1o6yjdU8yo3vNWXFGLqYVCyR_bSYFif_6csZNRvrWJ34/edit?usp=sharing"

conn = st.connection("gsheets", type=GSheetsConnection)

# קריאת הנתונים הקיימים
df = conn.read(spreadsheet=spreadsheet_url, usecols=[0, 1])
df = df.dropna(how="all")

# תפריט צד להוספה
st.sidebar.header("הוספת ספר חדש")
book_name = st.sidebar.text_input("שם הספר")
book_location = st.sidebar.text_input("מיקום הספר")

if st.sidebar.button("שמור במאגר"):
    if book_name and book_location:
        # יצירת שורה חדשה
        new_row = pd.DataFrame([{"שם הספר": book_name, "מיקום": book_location}])
        updated_df = pd.concat([df, new_row], ignore_index=True)
        
        # עדכון הגליון
        conn.update(spreadsheet=spreadsheet_url, data=updated_df)
        st.sidebar.success(f"הספר '{book_name}' נשמר!")
        st.rerun()
    else:
        st.sidebar.error("נא למלא את שני השדות")

# חיפוש
st.header("🔍 חיפוש ספר")
search_query = st.text_input("הקלידי שם לחיפוש:")

if search_query:
    results = df[df["שם הספר"].str.contains(search_query, case=False, na=False)]
    if not results.empty:
        st.table(results)
    else:
        st.warning("הספר לא נמצא במאגר")
else:
    st.write("כל הספרים במאגר:")
    st.dataframe(df, use_container_width=True)
