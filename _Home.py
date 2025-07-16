import streamlit as st
import streamlit_authenticator as stauth
import yaml
from yaml.loader import SafeLoader
import pandas as pd

# Authentication
# Convert st.secrets["auth_config"] to a *real dict recursively*
# Recursively convert st.secrets to a plain dict
def convert_secrets_to_dict(secrets_obj):
    if isinstance(secrets_obj, st.runtime.secrets.Secrets):
        return {k: convert_secrets_to_dict(v) for k, v in secrets_obj.items()}
    elif isinstance(secrets_obj, dict):
        return {k: convert_secrets_to_dict(v) for k, v in secrets_obj.items()}
    else:
        return secrets_obj

# Use the converter
config = convert_secrets_to_dict(st.secrets["auth_config"])

# Debugging: Check the structure of the config
st.write("Type of config:", type(config))
st.write("Type of credentials:", type(config.get("credentials")))
st.write("Type of usernames:", type(config["credentials"].get("usernames")))
st.write("Complete config structure:", config)

# Create the authenticator object
# authenticator = stauth.Authenticate(
#     config['credentials'],
#     config['cookie']['name'],
#     config['cookie']['key'],
#     config['cookie']['expiry_days']
# )

# Render the login widget
# name, authentication_status, username = authenticator.login()

# try:
#     authenticator.login()
# except Exception as e:
#     st.error(e)

# auth_status = st.session_state.get('authentication_status')

# if auth_status is False:
#     st.error('Username/password is incorrect')
#     st.stop()
# elif auth_status is None:
#     st.warning('Please enter your username and password')
#     st.stop()

# If we reach here, the user is authenticated
# authenticator.logout()
# st.write(f'Welcome *{st.session_state.get("name")}*')
# st.title('Some content')

# The rest of your app goes here
# st.write("Protected app content goes here.")