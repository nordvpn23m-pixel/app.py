import streamlit as st
import pandas as pd
import re
import io

st.set_page_config(page_title="OTP Extractor", layout="wide")

st.title("📊 SMS CDR OTP Extractor")
st.write("আপনার CSV ফাইলটি আপলোড করুন এবং স্বয়ংক্রিয়ভাবে OTP সংগ্রহ করুন।")

uploaded_file = st.file_uploader("Upload CSV File", type=["csv"])

def extract_otp(text):
    # ৬ থেকে ৮ ডিজিটের নম্বর খোঁজার জন্য Regex
    if isinstance(text, str):
        match = re.search(r'\b\d{6,8}\b', text)
        return match.group(0) if match else "No OTP"
    return "No OTP"

if uploaded_file is not None:
    try:
        # ফাইল পড়া (আপনার ফাইলের ফরম্যাট অনুযায়ী ২য় লাইন থেকে ডাটা শুরু হতে পারে)
        df = pd.read_csv(uploaded_file, skiprows=1)
        
        if 'SMS' in df.columns and 'Number' in df.columns:
            # OTP এক্সট্রাক্ট করা
            df['Extracted_OTP'] = df['SMS'].apply(extract_otp)
            
            # প্রয়োজনীয় কলামগুলো দেখানো
            result_df = df[['Number', 'Extracted_OTP', 'SMS']]
            
            st.success("Extraction Complete!")
            st.dataframe(result_df)
            
            # ডাউনলোড বাটন
            csv = result_df.to_csv(index=False).encode('utf-8')
            st.download_button(
                label="Download Extracted Data as CSV",
                data=csv,
                file_name='extracted_otp.csv',
                mime='text/csv',
            )
        else:
            st.error("ফাইলে 'SMS' এবং 'Number' কলাম খুঁজে পাওয়া যায়নি।")
    except Exception as e:
        st.error(f"Error: {e}")

st.markdown("---")
st.caption("Developed for Data Processing Purposes")
