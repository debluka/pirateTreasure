import firebase_admin
from firebase_admin import credentials
from firebase_admin import db

# Fetch the service account key JSON file contents
from firebase_admin.db import Reference

cred: any = credentials.Certificate('firestoreKey.json')

# Initialize the app with a service account, granting admin privileges
firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://piratestreasure-a3944-default-rtdb.europe-west1.firebasedatabase.app/'
})

# As an admin, the app has access to read and write all data, regardless of Security Rules
ref: Reference = db.reference('/')
