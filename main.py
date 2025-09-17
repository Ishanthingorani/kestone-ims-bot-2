import streamlit as st
import pandas as pd
from difflib import get_close_matches

st.set_page_config(page_title="Kestone IMS – Master Database", page_icon="📊", layout="wide")

st.image("kestone_logo.png", width=120)
st.title("Kestone IMS – Master Database")
st.markdown("🏢 **Company Info Bot (TEI Lookup)**")
st.markdown("Ask me about any company, and I’ll show you Turnover, Employee Range, and Industry Vertical!")

@st.cache_data
def load_data():
    return pd.read_excel("sample_data.xlsx")

df = load_data()

# Option selection
option = st.radio("Choose Mode:", ["Single Company Lookup", "Bulk Upload"])

if option == "Single Company Lookup":
    company_name = st.text_input("🔍 Enter Company Name")
    if company_name:
        matches = get_close_matches(company_name, df["Company Name"].tolist(), n=1, cutoff=0.4)
        if matches:
            result = df[df["Company Name"] == matches[0]]
            st.success("✅ Result Found")
            st.dataframe(result, use_container_width=True)
        else:
            st.error("❌ No match found")

elif option == "Bulk Upload":
    uploaded_file = st.file_uploader("Upload Excel file with Company Name column", type=["xlsx"])
    if uploaded_file:
        user_df = pd.read_excel(uploaded_file)
        if "Company Name" in user_df.columns:
            merged = user_df.merge(df, on="Company Name", how="left")
            st.dataframe(merged, use_container_width=True)
            st.download_button("📥 Download Results", merged.to_csv(index=False).encode("utf-8"), "results.csv", "text/csv")
        else:
            st.error("❌ Uploaded file must have a 'Company Name' column")
