from pymongo import MongoClient
import os

MONGO_URI = os.getenv("MONGO_URI", "mongodb+srv://atlas-sample-dataset-load-667e8d1682dd5d4c9373fe3f:i5DPqBZMG421XQky@crewai.2m15tm5.mongodb.net/?retryWrites=true&w=majority&appName=crewai")
DB_NAME = "licitatie_processor"

client = MongoClient(MONGO_URI)
db = client[DB_NAME]

def save_agent_configs(configs):
    db.agent_configs.replace_one({}, configs, upsert=True)

def load_agent_configs():
    configs = db.agent_configs.find_one()
    if not configs:
        return {
            "Manager": {"instructions": "", "backstory": ""},
            "Cercetător": {"instructions": "", "backstory": ""},
            "Scriitor": {"instructions": "", "backstory": ""},
            "Analist": {"instructions": "", "backstory": ""},
            "Expert Financiar": {"instructions": "", "backstory": ""}
        }
    return configs

def save_chat(user_id, chat_data):
    db.chats.insert_one({"user_id": user_id, "chat_data": chat_data})

def load_chats(user_id):
    return list(db.chats.find({"user_id": user_id}))