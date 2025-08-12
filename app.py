import streamlit as st

# Page settings
st.set_page_config(page_title="Group project MC - O31
ITIB4114-BUSINESS INTELLIGENCE
", layout="wide")

# Title
st.title("COVID-19 Data visualization and forcast ")

# Section: Group Members
st.header(" Group 5 Members")
group_members = [
    "1. CATHERINE ROSEY A/P PRAK CHUAB ",
    "2. MUHAMMAD LUKMAN BIN ROSDIN",
    "3. TRERAAJESREE A/P MANI DHANAPALAN",
    "4. MUHAMMAD RIDZUAN BIN SUTIMIN "
]
for member in group_members:
    st.write(member)

# Section: General Information with Crisis & Losses
st.header("ℹ General Information about COVID-19")
st.markdown("""
COVID-19 is a respiratory illness caused by the SARS-CoV-2 virus.  
It was first identified in December 2019 and quickly spread worldwide, leading to a global pandemic.  

Common symptoms include fever, cough, fatigue, and difficulty breathing.  
Prevention measures include wearing masks, maintaining physical distancing, frequent handwashing,  
and vaccination to reduce severe illness and death.

---

### 🆘  what covid had cause in Malaysia
- **Healthcare System Overload:** Hospitals, ICUs, and quarantine centres reached maximum capacity, forcing the setup of field hospitals and the mobilisation of army medical teams.
- **Economic Shutdowns:** Movement Control Orders (MCOs) repeatedly halted economic activities, causing massive disruption to SMEs, tourism, and manufacturing sectors.
- **Education Disruption:** Millions of students had to shift to online learning, exposing the digital divide between urban and rural areas.
- **Supply Chain Disruptions:** Shortages of medical supplies, PPE, oxygen tanks, and essential goods in certain regions.
- **Mental Health Strain:** Increased cases of depression, anxiety, and even suicide rates due to job losses, financial stress, and social isolation.

---

### 💔 Losses Faced in Malaysia
- **Human Loss:** Over 36,000 deaths recorded as of 2023, with thousands more suffering from long COVID symptoms.
- **Economic Loss:** Estimated RM500 billion in economic output lost between 2020–2022 due to lockdowns and reduced productivity.
- **Employment Loss:** Unemployment peaked at around 5.3% in May 2020, with many in tourism, retail, and F&B sectors severely affected.
- **Social & Cultural Loss:** Suspension of Hari Raya, Chinese New Year, Deepavali gatherings; cancellation of weddings and public events.
- **Educational Loss:** Learning gaps widened, with some students losing more than a year of effective education.

---

This dashboard aims to visualise the timeline and severity of these impacts, helping us understand the broader picture of the pandemic in Malaysia.
""")

# Section: Image from Repo
st.header("🖼 COVID-19 forcast")
st.image("images/covid_map.png", caption="Global COVID-19 Map", use_column_width=True)

# Tableau Dashboard Embed
st.header(" Data dashboard")
tableau_embed_code = """
<iframe src="https://public.tableau.com/views/Book1_17548411159820/Dashboard1?:language=en-US&:sid=&:redirect=auth&:display_count=n&:origin=viz_share_link"
width="100%" height="800px"></iframe>
"""
st.markdown(tableau_embed_code, unsafe_allow_html=True)
