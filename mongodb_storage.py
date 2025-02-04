import os
import streamlit as st
from pymongo import MongoClient
from pymongo.errors import ConnectionFailure

MONGO_URI = os.getenv("MONGO_URI")
DB_NAME = "licitatie_processor"

try:
    client = MongoClient(MONGO_URI, serverSelectionTimeoutMS=5000)
    client.admin.command('ismaster')
    db = client[DB_NAME]
    st.success("MongoDB connection successful")
except ConnectionFailure as e:
    st.error(f"MongoDB connection failed: {str(e)}")
    db = None

def save_agent_configs(configs):
    if db:
        db.agent_configs.replace_one({}, configs, upsert=True)
    else:
        st.warning("MongoDB connection is not available. Configurations will not be saved.")

def load_agent_configs():
    default_configs = {
        "Manager": {"instructions": "", "backstory": ""},
        "Cercetător": {"instructions": "", "backstory": ""},
        "Scriitor": {"instructions": "", "backstory": ""},
        "Analist": {"instructions": "", "backstory": ""},
        "Expert Financiar": {"instructions": "", "backstory": ""}
    }
    if db:
        try:
            configs = db.agent_configs.find_one()
            return configs if configs else default_configs
        except Exception as e:
            st.error(f"Error loading configurations: {str(e)}")
            return default_configs
    else:
        st.warning("MongoDB connection is not available. Using default configurations.")
        return default_configs
def save_chat(user_id, chat_data):
    db.chats.insert_one({"user_id": user_id, "chat_data": chat_data})

def load_chats(user_id):
    return list(db.chats.find({"user_id": user_id}))