import streamlit as st
from google.oauth2 import service_account
from googleapiclient.discovery import build

SCOPES = ['https://www.googleapis.com/auth/drive.file']

def get_drive_service():
    creds_dict = st.secrets["google_service_account"]
    creds = service_account.Credentials.from_service_account_info(
        creds_dict, scopes=SCOPES
    )
    return build("drive", "v3", credentials=creds)

def create_drive_folders(deliverables, parent_name="Creative Brief Project"):
    service = get_drive_service()
    folder_metadata = {
        'name': parent_name,
        'mimeType': 'application/vnd.google-apps.folder'
    }
    parent = service.files().create(body=folder_metadata, fields='id').execute()
    parent_id = parent.get('id')
    links = []
    for name in deliverables:
        folder = service.files().create(body={
            'name': name,
            'mimeType': 'application/vnd.google-apps.folder',
            'parents': [parent_id]
        }, fields='id').execute()
        links.append(f"https://drive.google.com/drive/folders/{folder['id']}")
    return links
