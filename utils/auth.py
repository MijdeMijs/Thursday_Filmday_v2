import streamlit as st
import streamlit_authenticator as stauth

def convert_attrdict_to_dict(attr_dict):
    """Recursively convert st.secrets.AttrDict to a normal dict"""
    if isinstance(attr_dict, st.runtime.secrets.AttrDict):
        return {k: convert_attrdict_to_dict(v) for k, v in attr_dict.items()}
    elif isinstance(attr_dict, dict):
        return {k: convert_attrdict_to_dict(v) for k, v in attr_dict.items()}
    else:
        return attr_dict

def get_authenticator():
    """Return a configured stauth.Authenticate object"""
    config = convert_attrdict_to_dict(st.secrets["auth_config"])
    authenticator = stauth.Authenticate(
        config["credentials"],
        config["cookie"]["name"],
        config["cookie"]["key"],
        config["cookie"]["expiry_days"],
    )
    return authenticator