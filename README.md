# 📁 Creative Brief Setup Agent

This Streamlit app helps convert creative briefs into structured data and creates Google Drive folders for deliverables using AI.

## ✨ Features

- Upload `.txt` creative brief
- AI parses goals, deliverables, key dates, and responsibilities
- Creates Google Drive folders automatically
- Supports both Cohere (v1) and Google Gemini (v2) backends

## 🚀 Deploy on Streamlit Cloud

1. Push to GitHub
2. Deploy via https://streamlit.io/cloud
3. Add your API keys in Streamlit Secrets Manager:

```toml
COHERE_API_KEY = "your-cohere-key"
GOOGLE_API_KEY = "your-gemini-key"
