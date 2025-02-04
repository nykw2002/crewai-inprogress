import streamlit as st
from mongodb_storage import save_agent_configs, load_agent_configs
from utils import save_to_knowledge_base, delete_from_knowledge_base, get_knowledge_base_files
from config import KNOWLEDGE_BASE_DIR

def setup_ui():
    load_custom_css()
    st.sidebar.title("Procesor de Documente pentru Licitații")
    
    agent_configs = load_agent_configs()
    
    # Knowledge Base Section
    st.sidebar.subheader("Baza de Cunoștințe")
    kb_files = st.sidebar.file_uploader("Încărcați fișiere în Baza de Cunoștințe", accept_multiple_files=True, key="kb_files_uploader")
    if kb_files:
        for file in kb_files:
            save_to_knowledge_base(file, KNOWLEDGE_BASE_DIR)
            st.sidebar.success(f"S-a adăugat {file.name} în Baza de Cunoștințe")

    # Display and manage Knowledge Base files
    st.sidebar.subheader("Fișiere curente în Baza de Cunoștințe")
    for idx, file in enumerate(get_knowledge_base_files(KNOWLEDGE_BASE_DIR)):
        col1, col2 = st.sidebar.columns([3, 1])
        col1.write(file)
        if col2.button("Șterge", key=f"delete_button_{idx}"):
            delete_from_knowledge_base(file, KNOWLEDGE_BASE_DIR)
            st.sidebar.success(f"S-a șters {file} din Baza de Cunoștințe")
            st.experimental_rerun()

    # Agent customization
    st.sidebar.subheader("Personalizare Agenți")
    agent_names = ["Manager", "Cercetător", "Scriitor", "Analist", "Expert Financiar"]
    for agent_name in agent_names:
        with st.sidebar.expander(f"Configurare {agent_name}"):
            agent_configs[agent_name]["instructions"] = st.text_area(
                f"Instrucțiuni {agent_name}", 
                value=agent_configs[agent_name]["instructions"],
                key=f"{agent_name}_instructions_input",
                max_chars=500
            )
            agent_configs[agent_name]["backstory"] = st.text_area(
                f"Povestea {agent_name}", 
                value=agent_configs[agent_name]["backstory"],
                key=f"{agent_name}_backstory_input",
                max_chars=500
            )

    save_config = st.sidebar.button("Salvează Configurările Agenților", key="save_config_button")

    if save_config:
        save_agent_configs(agent_configs)
        st.sidebar.success("Configurările au fost salvate cu succes!")

    return agent_configs, save_config

def chat_interface():
    user_input = st.text_input("Scrieți mesajul dvs. aici...")
    uploaded_file = st.file_uploader("Încărcați un fișier (opțional)", type=["txt", "pdf"])
    return user_input, uploaded_file

def display_result(result):
    st.subheader("Rezultatul Procesării")
    st.write(result)

def load_custom_css():
    st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Roboto:wght@300;400;700&display=swap');

    body {
        font-family: 'Roboto', sans-serif;
        background-color: #0f0f1a;
        color: #ffffff;
    }

    .stApp {
        background-color: rgba(15, 15, 26, 0.8);
    }

    .sidebar {
        background-color: rgba(26, 26, 46, 0.8);
        padding: 20px;
        border-radius: 10px;
        backdrop-filter: blur(10px);
        border: 1px solid rgba(255, 255, 255, 0.1);
    }

    .futuristic-title {
        font-size: 24px;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 2px;
        margin-bottom: 20px;
        text-shadow: 0 0 10px #4a4ae9;
        animation: glow 2s ease-in-out infinite alternate;
    }

    .message {
        margin-bottom: 15px;
        padding: 15px;
        border-radius: 20px;
        max-width: 80%;
        box-shadow: 0 4px 10px rgba(0, 0, 0, 0.3);
        background: linear-gradient(145deg, rgba(255,255,255,0.1) 0%, rgba(255,255,255,0.05) 100%);
        backdrop-filter: blur(5px);
        border: 1px solid rgba(255,255,255,0.1);
    }

    .futuristic-input {
        background-color: rgba(42, 42, 78, 0.6);
        border: none;
        border-radius: 5px;
        color: #ffffff;
        padding: 10px;
        margin-bottom: 10px;
        transition: all 0.3s ease;
    }

    .futuristic-input:focus {
        background-color: rgba(42, 42, 78, 0.8);
        box-shadow: 0 0 10px rgba(74, 74, 233, 0.5);
    }

    .futuristic-button {
        background-color: #4a4ae9;
        color: #ffffff;
        border: none;
        border-radius: 5px;
        padding: 10px 20px;
        cursor: pointer;
        transition: all 0.3s ease;
        text-transform: uppercase;
        letter-spacing: 1px;
    }

    .futuristic-button:hover {
        background-color: #3a3ad9;
        box-shadow: 0 0 15px rgba(74, 74, 233, 0.7);
        transform: translateY(-2px);
    }

    @keyframes glow {
        from { text-shadow: 0 0 5px #4a4ae9, 0 0 10px #4a4ae9, 0 0 15px #4a4ae9; }
        to { text-shadow: 0 0 10px #4a4ae9, 0 0 20px #4a4ae9, 0 0 30px #4a4ae9; }
    }
    </style>
    """, unsafe_allow_html=True)