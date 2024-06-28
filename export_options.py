import streamlit as st
import pdfkit
from docx import Document

def export_to_pdf(content, filename):
    pdfkit.from_string(content, filename)
    st.download_button(label="Download PDF", data=open(filename, "rb"), file_name=filename, mime="application/pdf")

def export_to_word(content, filename):
    doc = Document()
    doc.add_paragraph(content)
    doc.save(filename)
    st.download_button(label="Download Word", data=open(filename, "rb"), file_name=filename, mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document")

def export_to_html(content, filename):
    with open(filename, "w") as f:
        f.write(content)
    st.download_button(label="Download HTML", data=open(filename, "r"), file_name=filename, mime="text/html")