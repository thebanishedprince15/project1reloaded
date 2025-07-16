import streamlit as st
from google.oauth2 import service_account
from googleapiclient.discovery import build

SCOPES = ["https://www.googleapis.com/auth/drive.file"]

def get_drive_service():
    creds_dict = st.secrets["google_service_account"]
    creds = service_account.Credentials.from_service_account_info(
        creds_dict, scopes=SCOPES
    )
    service = build("drive", "v3", credentials=creds)
    return service

def create_drive_folders(deliverables, parent_name="Creative Brief Project"):
    service = get_drive_service()
    
    # Create main parent folder
    folder_metadata = {
        "name": parent_name,
        "mimeType": "application/vnd.google-apps.folder"
    }
    parent = service.files().create(body=folder_metadata, fields="id").execute()
    parent_id = parent.get("id")

    # Create subfolders for each deliverable
    links = []
    for name in deliverables:
        file_metadata = {
            "name": name,
            "mimeType": "application/vnd.google-apps.folder",
            "parents": [parent_id]
        }
        folder = service.files().create(body=file_metadata, fields="id").execute()
        folder_id = folder.get("id")
        links.append(f"https://drive.google.com/drive/folders/{folder_id}")

    return links
