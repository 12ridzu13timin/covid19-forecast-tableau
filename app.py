import streamlit as st

st.set_page_config(page_title="My Tableau Dashboard", layout="wide")

st.title("COVID-19 Dashboard 2020-2022")

st.markdown("""
MC - O31
ITIB4114-BUSINESS INTELLIGENCE
MAY 2025
GROUP 5
""")

tableau_embed_code = """
<iframe src="https://public.tableau.com/views/Book1_17548411159820/Dashboard1?:language=en-US&:sid=&:redirect=auth&:display_count=n&:origin=viz_share_link"
width="100%" height="800px"></iframe>
"""

st.markdown(tableau_embed_code, unsafe_allow_html=True)
