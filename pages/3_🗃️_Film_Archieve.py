#===============
# Imports
#===============
import streamlit as st
from utils.auth import get_authenticator

#====================
# Authentication
#====================
# Create the authenticator
authenticator = get_authenticator()

# Show the login widget
try:
    authenticator.login()
except Exception as e:
    st.error(e)
    st.stop()

# Check login status
auth_status = st.session_state.get('authentication_status')

if auth_status is False:
    st.error("Username/password is incorrect")
    st.stop()
elif auth_status is None:
    st.warning("Please enter your username and password")
    st.stop()

# If logged in, show logout in sidebar
authenticator.logout(location="sidebar")

st.write('🏗️ PAGE UNDER CONSTRUCTION 🚧👷')