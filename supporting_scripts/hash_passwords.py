import streamlit_authenticator as stauth

hashed_password = stauth.Hasher.hash("password1")

print(hashed_password)

# passwords = ["password1", "password2", "password3"]

# hashed_passwords = [stauth.Hasher.hash(p) for p in passwords]

# print(hashed_passwords)