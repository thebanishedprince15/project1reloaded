import streamlit as st
from brief_parser_cohere import parse_brief
from gdrive_uploader import create_drive_folders

st.set_page_config(page_title="Creative Brief Setup Agent", layout="centered")
st.title("📁 Creative Brief → Checklist + Folder Setup")

uploaded_file = st.file_uploader("Upload your creative brief (.txt)", type=["txt"])
if uploaded_file:
    brief_text = uploaded_file.read().decode("utf-8")
    st.subheader("📋 Parsed Brief Summary")
    result = parse_brief(brief_text)

    if "error" in result:
        st.error(f"❌ {result['error']}")
        st.text_area("Raw Output", result.get("raw_response", ""), height=150)
    else:
        st.json(result)

        if st.button("📁 Create Google Drive Folder"):
            links = create_drive_folders(result.get("deliverables", []))
            st.success("✅ Folders created successfully!")
            for link in links:
                st.markdown(f"- [📂 {link}]({link})")
