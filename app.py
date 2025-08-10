import streamlit as st

st.set_page_config(page_title="My Tableau Dashboard", layout="wide")

st.title("COVID-19 Dashboard (Tableau + Streamlit)")

st.markdown("""
This dashboard is powered by Tableau Public and embedded in Streamlit.
""")

# Replace this with your own Tableau Public embed link
tableau_embed_code = """
<iframe src="https://public.tableau.com/views/Book1_17548411159820/Dashboard1?:language=en-US&:sid=&:redirect=auth&:display_count=n&:origin=viz_share_link"
width="100%" height="800px"></iframe>
"""

st.markdown(tableau_embed_code, unsafe_allow_html=True)
