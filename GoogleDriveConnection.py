from googleapiclient.http import MediaFileUpload
from Google import Create_Service  # This assumes that your file is in my_proj/my_proj/Google.py

class GoogleDriveConnection:
    CLIENT_SECRET_FILE = 'client-secret.json'
    API_NAME = "drive"
    API_VERSION = "v3"
    SCOPES = ['https://www.googleapis.com/auth/drive']

    def __init__(self):
        return
    
    def loadFileGoogleDrive(self, filepath, filename):
        drive = Create_Service(self.CLIENT_SECRET_FILE, self.API_NAME, self.API_VERSION, self.SCOPES)

        datos = {
            "name": filename,
            "parents": [
                "1EJJMMAiPXTCzg7WON2GktW8cHkmWDGWC"
                ]
            }

        media = MediaFileUpload( filepath + "/" + filename, mimetype="text/csv")

        file = drive.files().create(
            body = datos,
            media_body = media
        ).execute()

        print(file)
        return