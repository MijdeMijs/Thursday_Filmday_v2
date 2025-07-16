import streamlit as st
import streamlit_authenticator as stauth
import yaml
from yaml.loader import SafeLoader
import pandas as pd

# Authentication

# Load your YAML config
# with open('auth_config.yaml') as file:
config = st.secrets["auth_config"]

# Create the authenticator object
authenticator = stauth.Authenticate(
    config['credentials'],
    config['cookie']['name'],
    config['cookie']['key'],
    config['cookie']['expiry_days']
)

# Render the login widget
# name, authentication_status, username = authenticator.login()

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
st.write(f'Welcome *{st.session_state.get("name")}*')
st.title('Some content')

# The rest of your app goes here
st.write("Protected app content goes here.")

if st.button("Press"):
    st.write("Hello world")