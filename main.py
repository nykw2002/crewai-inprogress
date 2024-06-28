import streamlit as st
from dotenv import load_dotenv
from advanced_agents import create_advanced_agents_and_crew
from ui_components import setup_ui, chat_interface, display_result, load_custom_css
from utils import process_file, get_knowledge_base_files
from config import KNOWLEDGE_BASE_DIR
from mongodb_storage import save_chat, load_chats
import uuid

load_dotenv()

def main():
    st.set_page_config(page_title="Procesor de Documente pentru Licitații", layout="wide")
    load_custom_css()
    
    agent_configs, save_config = setup_ui()

    # Initialize session state for user_id
    if 'user_id' not in st.session_state:
        st.session_state.user_id = str(uuid.uuid4())

    # Main content area
    st.title("Procesor de Documente pentru Licitații")
    
    st.write("Bine ați venit la procesorul nostru de documente pentru licitații!")
    st.write("Utilizați interfața de chat de mai jos pentru a interacționa cu agenții noștri.")

    # Chat interface
    user_input, uploaded_file = chat_interface()

    if user_input or uploaded_file:
        with st.spinner("Se procesează..."):
            try:
                manager, crew = create_advanced_agents_and_crew(agent_configs)
                input_data = user_input or ""
                file_summary = ""
                if uploaded_file:
                    _, file_summary = process_file(uploaded_file)
                    input_data += f"\n\nUn fișier a fost încărcat. Iată un rezumat al conținutului său: {file_summary}"

                knowledge_base_used = len(get_knowledge_base_files(KNOWLEDGE_BASE_DIR)) > 0
                if knowledge_base_used:
                    input_data += "\n\nInformațiile din baza de cunoștințe sunt disponibile pentru această sarcină."

                result = crew.process(input_data, knowledge_base_used, file_summary)
                display_result(result)

                # Save chat to MongoDB
                chat_data = {
                    "user_input": user_input,
                    "file_name": uploaded_file.name if uploaded_file else None,
                    "result": result
                }
                save_chat(st.session_state.user_id, chat_data)

            except Exception as e:
                st.error(f"A apărut o eroare: {str(e)}")
                st.exception(e)

if __name__ == "__main__":
    main()