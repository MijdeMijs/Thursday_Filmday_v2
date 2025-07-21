#===============
# Imports
#===============
import streamlit as st
from utils.auth import get_authenticator
import pandas as pd
import time
from datetime import datetime
import random
import sqlite3

#====================
# Authentication
#====================
# # Create the authenticator
# authenticator = get_authenticator()

# # Show the login widget
# try:
#     authenticator.login()
# except Exception as e:
#     st.error(e)
#     st.stop()

# # Check login status
# auth_status = st.session_state.get('authentication_status')

# if auth_status is False:
#     st.error("Username/password is incorrect")
#     st.stop()
# elif auth_status is None:
#     st.warning("Please enter your username and password")
#     st.stop()

# # If logged in, show logout in sidebar
# authenticator.logout(location="sidebar")

st.write('🏗️ PAGE UNDER CONSTRUCTION 🚧👷')

#=============
# Sidebar
#=============

# Sidebar: Random Film Button
st.sidebar.title("Random Film Generator")

st.sidebar.write("""Can't decide what to watch? Let our Random Film Generator 
                 choose for you! Click the button and let faith decide!
                 Enjoy your movie night! 🍿🎥""")

if st.sidebar.button("Random film!"):
    def random_film ():
        conn = sqlite3.connect("data/film_database.db")
        cursor = conn.cursor()
        cursor.execute("""
            SELECT *
            FROM film_data
            ORDER BY RANDOM()
            LIMIT 1
        """)
        random_choice = cursor.fetchone()
        conn.close()
        return random_choice

    # Run random_film()
    random_movie = random_film()

    # List of funny texts
    funny_texts = [
        "Reading your aura...",
        "Taming a monkey...",
        "Brewing some coffee...",
        "Counting stars...",
        "Feeding the unicorns...",
        "Polishing the pixels...",
        "Summoning good vibes...",
        "Tickling the code...",
        "Charging the flux capacitor...",
        "Aligning the planets...",
        "Petting the cat...",
        "Warming up the servers...",
        "Finding Waldo...",
        "Herding cats...",
        "Sharpening pencils...",
        "Calibrating the matrix...",
        "Baking cookies...",
        "Inflating balloons...",
        "Painting rainbows...",
        "Hacking the mainframe...",
        "Teleporting data...",
        "Tickling the electrons...",
        "Spinning up the hamster wheel...",
        "Inflating the internet...",
        "Waking up the servers...",
        "Unleashing the magic...",
        "Mixing the potions...",
        "Charging the crystals...",
        "Consulting the oracle...",
        "Tuning the algorithms...",
        "Rebooting the matrix...",
        "Casting spells...",
        "Brewing the potion...",
        "Hunting for Easter eggs...",
        "Rewiring the circuits...",
        "Synchronizing the clocks...",
        "Lubricating the gears...",
        "Recalibrating the sensors...",
        "Recharging the batteries...",
        "Assembling the pixels..."
    ]

    # Randomly choose a funny text
    progress_text = random.choice(funny_texts)

    # Create a progress bar
    my_bar = st.sidebar.progress(0)
       
    # Randomly choose a duration between 0.1 and 2 seconds
    duration = random.uniform(0.1, 1.5)

    # Calculate the sleep time per iteration
    sleep_time = duration / 100

    for percent_complete in range(100):
        time.sleep(sleep_time)
        my_bar.progress(percent_complete + 1, text=progress_text)

    time.sleep(1)
    my_bar.empty()

    st.sidebar.write(f'''
                     Maybe you'd like to watch **{random_movie[2]}**?
                     
                     **Rating: {random_movie[38]} | 
                     Duration: {random_movie[4]} min.** |
                     **Year: {random_movie[3]}**
                     ''')

    # Define IMDb URL
    random_url = f'https://www.imdb.com/title/{random_movie[0]}/'

    st.sidebar.link_button('Visit IMDb page!', random_url)

# ===============================
# region Archive intoduction
# ===============================

st.header("🗂️ Film Archive", divider="rainbow")

st.write('''The Film Archive is a comprehensive hub where you can revisit all the films 
         we’ve enjoyed together. It lets you see which room suggested each film, track 
         how many votes each room received, and even check out the movie snack of the 
         night. You can explore the archive by individual movie nights or view the entire 
         collection in one go. Each film entry is enriched with additional IMDb 
         information, providing a quick overview of key details. For added convenience, 
         there’s a dedicated IMDb film page button, so you can instantly visit the 
         official page for any movie. It’s the perfect way to relive past movie nights 
         and discover new favorites!''')