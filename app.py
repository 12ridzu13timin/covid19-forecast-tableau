import streamlit as st

# Page settings
st.set_page_config(page_title="GROUP PROJECT BUSINESS INTELLIGENCE", layout="wide")

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
st.image("images/forcast .png", caption="Global COVID-19 Map", use_column_width=True)

# Tableau Dashboard Embed
st.header(" Data dashboard")
tableau_embed_code = """
<iframe src="<div class='tableauPlaceholder' id='viz1754984144511' style='position: relative'><noscript><a href='#'><img alt=' ' src='https:&#47;&#47;public.tableau.com&#47;static&#47;images&#47;Bo&#47;Book1_17548411159820&#47;Dashboard1&#47;1_rss.png' style='border: none' /></a></noscript><object class='tableauViz'  style='display:none;'><param name='host_url' value='https%3A%2F%2Fpublic.tableau.com%2F' /> <param name='embed_code_version' value='3' /> <param name='site_root' value='' /><param name='name' value='Book1_17548411159820&#47;Dashboard1' /><param name='tabs' value='yes' /><param name='toolbar' value='yes' /><param name='static_image' value='https:&#47;&#47;public.tableau.com&#47;static&#47;images&#47;Bo&#47;Book1_17548411159820&#47;Dashboard1&#47;1.png' /> <param name='animate_transition' value='yes' /><param name='display_static_image' value='yes' /><param name='display_spinner' value='yes' /><param name='display_overlay' value='yes' /><param name='display_count' value='yes' /><param name='language' value='en-US' /></object></div>                <script type='text/javascript'>                    var divElement = document.getElementById('viz1754984144511');                    var vizElement = divElement.getElementsByTagName('object')[0];                    if ( divElement.offsetWidth > 800 ) { vizElement.style.minWidth='420px';vizElement.style.maxWidth='100%';vizElement.style.minHeight='610px';vizElement.style.maxHeight=(divElement.offsetWidth*0.75)+'px';} else if ( divElement.offsetWidth > 500 ) { vizElement.style.minWidth='420px';vizElement.style.maxWidth='100%';vizElement.style.minHeight='610px';vizElement.style.maxHeight=(divElement.offsetWidth*0.75)+'px';} else { vizElement.style.width='100%';vizElement.style.minHeight='1700px';vizElement.style.maxHeight=(divElement.offsetWidth*1.77)+'px';}                     var scriptElement = document.createElement('script');                    scriptElement.src = 'https://public.tableau.com/javascripts/api/viz_v1.js';                    vizElement.parentNode.insertBefore(scriptElement, vizElement);                </script>"
width="100%" height="800px"></iframe>
"""
st.markdown(tableau_embed_code, unsafe_allow_html=True)
