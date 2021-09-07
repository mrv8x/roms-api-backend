import firebase_admin

from firebase_admin import credentials, firestore, db
from loguru import logger


class FirebaseDatabase:
    def __init__(self, firebase_cert, project_id, firebase_rldb, rldb_builds):
        """ initialize authenticated GDrive Object """
        cred = credentials.Certificate(firebase_cert)
        firebase_admin.initialize_app(cred, {"projectId": project_id})
        self.__db = firestore.client()
        self.__db_rldb = db.reference(url=firebase_rldb)
        self.__db_rldb_builds = rldb_builds

    def create_user(self, collection, username, data):
        """
        Creates an user as a document of the collection user
        collection: collection name
        username: username
        data: document as dict
        """
        self.__db.collection(collection).document(username).set(data)
        logger.info(f"Adding {collection} {username} as a maintainer")

    def get_user(self, username, collection):
        return self.__db.collection(collection).document(username).get()

    def delete_user(self, username, collection):
        return self.__db.collection(collection).document(username).delete()

    def get_rldb(self):
        return self.__db_rldb

    def get_builds_rldb(self):

        rldb = self.get_rldb()
        return rldb.child(self.__db_rldb_builds)

    def add_build(
        self,
        file_id: str,
        time: float,
        username: str,
        version: str,
        codename: str,
        changelog: str,
    ):
        device_ref = self.get_builds_rldb().child(codename).child(version)

        new_build_ref = device_ref.push()
        new_build_ref.set(
            {
                "gdrive_file_id": file_id,
                "timestamp": time,
                "uploader_username": username,
                "changelog": changelog,
            }
        )

    def get_build_link(self, codename, version):
        try:
            rldb = self.__db_rldb.get().get("builds").get(codename).get(version)
            file_id = rldb.get(next(iter(rldb))).get(
                "gdrive_file_id"
            )  # gets only the latest builds
            return f"https://drive.google.com/uc?export=download&id={file_id}"  # direct download link
        except AttributeError:
            return None
