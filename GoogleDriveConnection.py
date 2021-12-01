from typing import Any
from googleapiclient.http import MediaFileUpload
from Google import Create_Service  # This assumes that your file is in my_proj/my_proj/Google.py
from JSONHandler import JSONHandler
import json

class GoogleDriveConnection:
    CLIENT_SECRET_FILE = 'client-secret.json'
    API_NAME = "drive"
    API_VERSION = "v3"
    SCOPES = ['https://www.googleapis.com/auth/drive']
    __jsonHandler = None
    __saved_files = {}

    def __init__(self):
        self.__jsonHandler = JSONHandler()
        return

    def createNewFileDrive(self, drive, datos, media):
        f = drive.files().create(
            body = datos,
            media_body = media
        ).execute()
        return f

    def updateFileDrive(self, drive, datos, media):
        f = drive.files().update(
            fileId = datos["fileId"],
            addParents = datos["parents"].pop(),
            media_body = media,
            body = {"name" : datos["name"]}
        ).execute()
        return f
    
    def loadFileGoogleDrive(self, filepath, filename):
        j = self.__jsonHandler.getJSON("saved_files.json")
        drive = Create_Service(self.CLIENT_SECRET_FILE, self.API_NAME, self.API_VERSION, self.SCOPES)

        datos = {
            "name": filename,
            "parents": [
                "1EJJMMAiPXTCzg7WON2GktW8cHkmWDGWC"
                ]
            }

        media = MediaFileUpload( filepath + "/" + filename, mimetype="text/csv")

        if self.__jsonHandler.keyExists(json.dumps(j), filename) :
            datos.update({"fileId" : j[filename]})
            file = self.updateFileDrive(drive, datos, media)
        else:
            file = self.createNewFileDrive(drive, datos, media)
            
        self.__saved_files.update({file["name"] : file["id"]})
        return

    def generateNewSavedFilesJSON(self):
        self.__jsonHandler.writeJSON("saved_files.json", self.__saved_files)
        return