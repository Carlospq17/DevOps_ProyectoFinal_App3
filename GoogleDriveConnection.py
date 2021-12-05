import re
import logging
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
        logging.debug('Creando nuevo archivo en la carpeta de Google Drive ' + str(f))
        return f

    def updateFileDrive(self, drive, datos, media):
        f = drive.files().update(
            fileId = datos["fileId"],
            addParents = datos["parents"].pop(),
            media_body = media,
            body = {"name" : datos["name"]}
        ).execute()
        logging.debug('Actualiza archivo ' + str(f) + ' en la carpeta de Google Drive')
        return f
    
    def loadFileGoogleDrive(self, filepath, filename):
        logging.debug("Cargar archivo al google drive: " + filepath + "/" + filename)
        j = self.__jsonHandler.getJSON("saved_files.json")
        drive = Create_Service(self.CLIENT_SECRET_FILE, self.API_NAME, self.API_VERSION, self.SCOPES)

        datos = {
            "name": filename,
            "parents": [
                "1EJJMMAiPXTCzg7WON2GktW8cHkmWDGWC"
                ]
            }

        media = MediaFileUpload( filepath + "/" + filename, mimetype="text/csv")
        logging.debug('Archivo cargado ' + str(media) + ' para guardarlo en Google Drive')

        if self.__jsonHandler.keyExists(json.dumps(j), re.split("(.*_)", filename)[1]) : #aplicar la expresion regular apropiada
            datos.update({"fileId" : j[re.split("(.*_)", filename)[1]]})
            file = self.updateFileDrive(drive, datos, media)
        else:
            file = self.createNewFileDrive(drive, datos, media)
            
        self.__saved_files.update({re.split("(.*_)", file["name"])[1] : file["id"]}) #guardar utilizando expresion regular apropiada
        return

    def generateNewSavedFilesJSON(self):
        logging.info("Generando nuevo JSON para archivos guardados")
        self.__jsonHandler.writeJSON("saved_files.json", self.__saved_files)
        return