import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
import os

# Use a service account.
cred = credentials.Certificate(os.path.dirname(__file__)+'/db.json')

app = firebase_admin.initialize_app(cred)

db = firestore.client()



def test():
  doc_ref = db.collection("users").document("alovelace")
  doc_ref.set({"first": "Ada", "last": "Lovelace", "born": 1815})