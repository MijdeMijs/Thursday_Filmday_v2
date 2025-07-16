import streamlit as st
import streamlit_authenticator as stauth
import yaml
from yaml.loader import SafeLoader
import pandas as pd

# Authentication
# Recursively convert st.secrets (AttrDict) to a normal dictionary
def convert_attrdict_to_dict(attr_dict):
    if isinstance(attr_dict, st.runtime.secrets.AttrDict):
        return {k: convert_attrdict_to_dict(v) for k, v in attr_dict.items()}
    elif isinstance(attr_dict, dict):
        return {k: convert_attrdict_to_dict(v) for k, v in attr_dict.items()}
    else:
        return attr_dict

# Use the converter to handle the secrets
config = convert_attrdict_to_dict(st.secrets["auth_config"])

# Create the authenticator object with the converted config
authenticator = stauth.Authenticate(
    config["credentials"],
    config["cookie"]["name"],
    config["cookie"]["key"],
    config["cookie"]["expiry_days"],
)

try:
    authenticator.login()
except Exception as e:
    st.error(e)

auth_status = st.session_state.get('authentication_status')

if auth_status is False:
    st.error('Username/password is incorrect')
    st.stop()
elif auth_status is None:
    st.warning('Please enter your username and password')
    st.stop()

# If we reach here, the user is authenticated
authenticator.logout()

# Title
st.title("Thursday Filmday :clapper::film_projector:")

# Web page introduction
st.write(f"""
    Hi {st.session_state.get("name")}, welcome to **Thursday Filmday**! 🎬

    This app is designed to enhance your movie night experience with three 
    exciting sections:

    1. **Film Chooser**: This section helps you select the perfect film 
       for your movie night. Whether you're in the mood for a comedy, 
       drama, or action-packed thriller, the Film Chooser will guide 
       you to the best options.
""")

# st.page_link("pages/1_🎬_Film_Chooser.py", label="Go to Film Chooser", icon="🎬")

st.write("""
    2. **Movie Stats**: Dive into some fun statistics about all the movies 
         we've watched together. Discover interesting trends, favorite 
         genres, and more. It's a great way to see our collective 
         movie-watching habits!
    """)

# st.page_link("pages/2_📊_Movie_Stats.py", label="Go to Movie Stats", icon="📊")

st.write("""
    3. **Film Archive**: Here, you can browse through a comprehensive list 
         of all the films we've watched and suggested. It's a handy 
         reference to revisit past favorites or find new recommendations.
    """)

# st.page_link("pages/3_🗂️_Film_Archieve.py", label="Go to Film Archieve", icon="🗂️")

st.write("""
    I've also hidden some fun easter eggs throughout the app for you to 
         discover. I put a lot of effort into creating this page, so I 
         hope you enjoy it. Please be gentle, as the app might not be the 
         most efficient in the world.

    Enjoy your movie night and happy watching! :popcorn:
    """)