import firebase_admin
from firebase_admin import credentials, firestore
from datetime import datetime
import os
import json


if not firebase_admin._apps:

    firebase_json = os.getenv("FIREBASE_KEY")

    if firebase_json:
        cred = credentials.Certificate(json.loads(firebase_json))
    else:
        cred = credentials.Certificate("firebase_key.json")

    firebase_admin.initialize_app(cred)


db = firestore.client()


def get_player(uid):
    doc = db.collection("players").document(uid).get()

    if doc.exists:
        return doc.to_dict()

    return None


def save_player(uid, data):
    db.collection("players").document(uid).set(
        data,
        merge=True
    )


def add_history(uid, event):
    db.collection("players").document(uid)\
    .collection("history").add({
        "event": event,
        "time": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    })