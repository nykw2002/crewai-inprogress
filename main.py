import streamlit as st
from dotenv import load_dotenv
from advanced_agents import create_advanced_agents_and_crew
from ui_components import setup_ui, chat_interface, display_result, load_custom_css
from utils import process_file, get_knowledge_base_files
from config import KNOWLEDGE_BASE_DIR
from mongodb_storage import save_chat, load_chats
from task_specific_agents import LegalAnalyst, TechnicalWriter, ProjectManager
from dynamic_agent_creation import create_custom_agent
from conflict_resolution import resolve_conflicts
from multi_language_support import process_multi_language
from data_visualization import create_chart
from document_comparison import compare_documents
from timeline_generation import generate_timeline
from sentiment_analysis import analyze_sentiment
from automatic_summarization import summarize_text
from citation_tracking import track_sources
from collaborative_editing import collaborative_edit
from export_options import export_to_pdf, export_to_word, export_to_html
import uuid
import os

load_dotenv()

def main():
    st.set_page_config(page_title="Procesor de Documente pentru Licitații", layout="wide")
    load_custom_css()
    
    agent_configs, save_config = setup_ui()

    if 'user_id' not in st.session_state:
        st.session_state.user_id = str(uuid.uuid4())

    st.title("Procesor de Documente pentru Licitații")
    
    st.write("Bine ați venit la procesorul nostru de documente pentru licitații!")
    st.write("Utilizați interfața de chat de mai jos pentru a interacționa cu agenții noștri.")

    # New feature selection
    feature = st.selectbox("Selectați o funcționalitate:", 
                           ["Chat Standard", "Analiză Juridică", "Scriere Tehnică", "Management de Proiect", 
                            "Agent Personalizat", "Analiză Multi-lingvistică", "Vizualizare Date", 
                            "Comparare Documente", "Generare Cronologie", "Analiză Sentiment", 
                            "Sumarizare Automată", "Editare Colaborativă", "Export"])

    if feature == "Chat Standard":
        user_input, uploaded_file = chat_interface()
    elif feature == "Analiză Juridică":
        user_input = st.text_area("Introduceți textul pentru analiză juridică:")
        uploaded_file = st.file_uploader("Încărcați un document juridic (opțional)")
    elif feature == "Scriere Tehnică":
        user_input = st.text_area("Introduceți specificațiile pentru documentul tehnic:")
    elif feature == "Management de Proiect":
        user_input = st.text_area("Introduceți cerințele proiectului:")
    elif feature == "Agent Personalizat":
        name = st.text_input("Numele agentului:")
        role = st.text_input("Rolul agentului:")
        instructions = st.text_area("Instrucțiuni pentru agent:")
        backstory = st.text_area("Povestea agentului:")
        if st.button("Creează Agent"):
            new_agent = create_custom_agent(name, role, instructions, backstory)
            st.success(f"Agent {name} creat cu succes!")
    elif feature == "Analiză Multi-lingvistică":
        user_input = st.text_area("Introduceți textul pentru analiză (în orice limbă):")
        target_language = st.selectbox("Selectați limba țintă:", ["en", "ro", "fr", "de", "es"])
    elif feature == "Vizualizare Date":
        user_input = st.text_area("Introduceți datele pentru vizualizare (format JSON):")
        chart_type = st.selectbox("Selectați tipul de grafic:", ["bar", "pie", "line"])
    elif feature == "Comparare Documente":
        doc1 = st.text_area("Introduceți primul document:")
        doc2 = st.text_area("Introduceți al doilea document:")
    elif feature == "Generare Cronologie":
        user_input = st.text_area("Introduceți textul pentru extragerea datelor:")
    elif feature == "Analiză Sentiment":
        user_input = st.text_area("Introduceți textul pentru analiza sentimentului:")
    elif feature == "Sumarizare Automată":
        user_input = st.text_area("Introduceți textul pentru sumarizare:")
        ratio = st.slider("Selectați raportul de sumarizare:", 0.1, 0.5, 0.2)
    elif feature == "Editare Colaborativă":
        collaborative_edit("document_1")
    elif feature == "Export":
        content = st.text_area("Introduceți conținutul pentru export:")
        export_format = st.selectbox("Selectați formatul de export:", ["PDF", "Word", "HTML"])

    if st.button("Procesează") and (user_input or uploaded_file):
        with st.spinner("Se procesează..."):
            try:
                if feature == "Chat Standard":
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
                elif feature == "Analiză Juridică":
                    legal_analyst = LegalAnalyst("Analist Juridic", "Analizează aspecte juridice", "Expert în drept")
                    result = legal_analyst.analyze_legal_document(user_input)
                elif feature == "Scriere Tehnică":
                    tech_writer = TechnicalWriter("Scriitor Tehnic", "Scrie documente tehnice", "Expert în documentație tehnică")
                    result = tech_writer.write_technical_document(user_input)
                elif feature == "Management de Proiect":
                    project_manager = ProjectManager("Manager de Proiect", "Creează planuri de proiect", "Expert în management de proiect")
                    result = project_manager.create_project_plan(user_input)
                elif feature == "Analiză Multi-lingvistică":
                    result = process_multi_language(user_input, create_advanced_agents_and_crew(agent_configs)[1], target_language)
                elif feature == "Vizualizare Date":
                    import json
                    data = json.loads(user_input)
                    create_chart(data, chart_type)
                    result = "Grafic generat cu succes!"
                elif feature == "Comparare Documente":
                    result = compare_documents(doc1, doc2)
                elif feature == "Generare Cronologie":
                    timeline = generate_timeline(user_input)
                    result = "\n".join([date.strftime("%Y-%m-%d") for date in timeline])
                elif feature == "Analiză Sentiment":
                    sentiment = analyze_sentiment(user_input)
                    result = f"Sentimentul textului este: {sentiment}"
                elif feature == "Sumarizare Automată":
                    result = summarize_text(user_input, ratio)
                elif feature == "Export":
                    if export_format == "PDF":
                        export_to_pdf(content, "export.pdf")
                    elif export_format == "Word":
                        export_to_word(content, "export.docx")
                    else:
                        export_to_html(content, "export.html")
                    result = "Fișier exportat cu succes!"
                
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