import streamlit as st
from datetime import datetime

def collaborative_edit(document_key):
    if document_key not in st.session_state:
        st.session_state[document_key] = ""
    
    edited_text = st.text_area("Edit document", st.session_state[document_key])
    
    if edited_text != st.session_state[document_key]:
        st.session_state[document_key] = edited_text
        st.session_state.setdefault('edit_history', []).append({
            'timestamp': datetime.now().isoformat(),
            'content': edited_text
        })

    if st.button("View Edit History"):
        for edit in st.session_state.get('edit_history', []):
            st.write(f"{edit['timestamp']}: {edit['content'][:50]}...")