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

# Debugging: Check the structure of the config
st.write("Type of config:", type(config))  # Should print <class 'dict'>
st.write("Type of credentials:", type(config.get("credentials")))  # Should print <class 'dict'>
st.write("Type of usernames:", type(config["credentials"].get("usernames")))  # Should print <class 'dict'>
st.write("Complete config structure:", config)

# Create the authenticator object with the converted config
authenticator = stauth.Authenticate(
    config["credentials"],
    config["cookie"]["name"],
    config["cookie"]["key"],
    config["cookie"]["expiry_days"],
)

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