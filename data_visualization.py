import streamlit as st
import plotly.graph_objects as go

def create_chart(data, chart_type='bar'):
    if chart_type == 'bar':
        fig = go.Figure(data=[go.Bar(x=list(data.keys()), y=list(data.values()))])
    elif chart_type == 'pie':
        fig = go.Figure(data=[go.Pie(labels=list(data.keys()), values=list(data.values()))])
    st.plotly_chart(fig)