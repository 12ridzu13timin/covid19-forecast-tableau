import streamlit as st

# Page settings
st.set_page_config(page_title="COVID-19 Dashboard Info", layout="wide")

# Title
st.title("COVID-19 Dashboard Information")

# Section: Group Members
st.header("👥 Our Group Members")
group_members = [
    "1. Alice Tan Wei Ling",
    "2. Muhammad Ridzuan Sutimin",
    "3. John Lim Wei Han",
    "4. Nur Aisyah Binti Ahmad"
]
for member in group_members:
    st.write(member)

# Section: General Information
st.header("ℹ️ General Information about COVID-19")
st.markdown("""
COVID-19 is a respiratory illness caused by the SARS-CoV-2 virus.  
It was first identified in December 2019 and quickly spread worldwide, leading to a global pandemic.  
Common symptoms include fever, cough, fatigue, and difficulty breathing.  
Prevention measures include wearing masks, maintaining physical distancing, frequent handwashing,  
and vaccination to reduce severe illness and death.
""")

# Section: Image from Repo
st.header("🖼️ COVID-19 Illustration")
st.image("images/covid_map.png", caption="Global COVID-19 Map", use_column_width=True)
# Make sure your image is in a folder called 'images' in your repo

# Optional: Add Tableau Dashboard Embed
st.header("📊 Interactive Dashboard")
tableau_embed_code = """
<iframe src="<div class='tableauPlaceholder' id='viz1754983133047' style='position: relative'><noscript><a href='#'><img alt=' ' src='https:&#47;&#47;public.tableau.com&#47;static&#47;images&#47;Bo&#47;Book1_17548411159820&#47;Dashboard1&#47;1_rss.png' style='border: none' /></a></noscript><object class='tableauViz'  style='display:none;'><param name='host_url' value='https%3A%2F%2Fpublic.tableau.com%2F' /> <param name='embed_code_version' value='3' /> <param name='site_root' value='' /><param name='name' value='Book1_17548411159820&#47;Dashboard1' /><param name='tabs' value='yes' /><param name='toolbar' value='yes' /><param name='static_image' value='https:&#47;&#47;public.tableau.com&#47;static&#47;images&#47;Bo&#47;Book1_17548411159820&#47;Dashboard1&#47;1.png' /> <param name='animate_transition' value='yes' /><param name='display_static_image' value='yes' /><param name='display_spinner' value='yes' /><param name='display_overlay' value='yes' /><param name='display_count' value='yes' /><param name='language' value='en-US' /></object></div>                <script type='text/javascript'>                    var divElement = document.getElementById('viz1754983133047');                    var vizElement = divElement.getElementsByTagName('object')[0];                    if ( divElement.offsetWidth > 800 ) { vizElement.style.minWidth='420px';vizElement.style.maxWidth='100%';vizElement.style.minHeight='610px';vizElement.style.maxHeight=(divElement.offsetWidth*0.75)+'px';} else if ( divElement.offsetWidth > 500 ) { vizElement.style.minWidth='420px';vizElement.style.maxWidth='100%';vizElement.style.minHeight='610px';vizElement.style.maxHeight=(divElement.offsetWidth*0.75)+'px';} else { vizElement.style.width='100%';vizElement.style.minHeight='1700px';vizElement.style.maxHeight=(divElement.offsetWidth*1.77)+'px';}                     var scriptElement = document.createElement('script');                    scriptElement.src = 'https://public.tableau.com/javascripts/api/viz_v1.js';                    vizElement.parentNode.insertBefore(scriptElement, vizElement);                </script>"
width="100%" height="800px"></iframe>
"""
st.markdown(tableau_embed_code, unsafe_allow_html=True)
