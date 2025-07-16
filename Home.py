#===============
# Imports
#===============
import streamlit as st
import streamlit_authenticator as stauth
from utils.auth import get_authenticator
import time
import random

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

#=============
# Sidebar
#=============

# Sidebar: Random Film Button
st.sidebar.title("Random Film Generator")

st.sidebar.write("Can't decide what to watch? Let our Random Film Generator choose for you! Click the button and get a film title, IMDb rating, and duration. Enjoy your movie night! 🍿🎥")

if st.sidebar.button("Generate random film!"):
    # Check if the data is ready
    if "filtered_data" in st.session_state:
        # Sample one row
        random_row = st.session_state["filtered_data"].sample(1)

        # Extract the required data
        random_film = random_row["Film"].iloc[0]
        random_rating = random_row["IMDb Rating"].iloc[0]
        random_duration = random_row["Duration"].iloc[0]
        random_year = random_row["Year"].iloc[0]
        random_ID = random_row["ID"].iloc[0]

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
        duration = random.uniform(0.1, 2)

        # Calculate the sleep time per iteration
        sleep_time = duration / 100

        for percent_complete in range(100):
            time.sleep(sleep_time)
            my_bar.progress(percent_complete + 1, text=progress_text)

        time.sleep(1)
        my_bar.empty()
        
        st.sidebar.write(f'''
                         Maybe you'd like to watch **{random_film}**?
                         
                         **Rating: {random_rating.round(1)} | 
                         Duration: {int(random_duration)}** |
                         **Year: {int(random_year)}**
                         ''')
        
        # Define IMDb URL
        random_url = f'https://www.imdb.com/title/{random_ID}/'

        st.sidebar.link_button('Visit IMDb page!', random_url)

    else:
        # Centered warning text using Markdown and CSS
        st.sidebar.markdown(
            """
            <div style="text-align: center; background-color: #FFA726; padding: 10px; border: 1px solid #ffa500; border-radius: 5px; color: black;">
                <strong>⚠️ First select filters! ⚠️</strong>
            </div>
            """,
            unsafe_allow_html=True,
        )
        st.sidebar.write('')
        # st.sidebar.page_link("pages/1_🎬_Film_Chooser.py", label="Go to Film Chooser", icon="🎬")
        
#=============
# Content
#=============

# Title
st.title("Thursday Filmday :clapper::film_projector:")

# Web page introduction
st.write(f"""
    Hi **{st.session_state.get("name")}**, welcome to **Thursday Filmday**! :clapper:

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

# ===========
# Footer
# ===========

# Custom CSS to adapt the footer to the browser's theme settings
st.markdown("""
    <style>
    @media (prefers-color-scheme: dark) {
        .footer {
            background-color: #333333;
            color: #FFFFFF;
        }
    }
    @media (prefers-color-scheme: light) {
        .footer {
            background-color: #f9f9f9;
            color: #6c757d;
        }
    }
    .footer {
             width: 100%;
             text-align: center;
             align-items: center;
             padding: 5px 10px 5px 10px;
             margin-top: 20px;
             margin-bottom: 0px;
             font-size: 14px;
         }
    </style>
     <div class="footer">
         <p>The Thursday Filmday app was made possible by Midas, the man who hesitated 
            for so long about which movie to watch that he developed a movie app in the 
            meantime - <a href="https://eelslap.com/" target="_blank">ADHD hyperfocus</a> - 
            <a href="https://streamlit.io/" target="_blank">Streamlit</a> - 
            <a href="https://developer.imdb.com/" target="_blank">IMDb Developer</a> and
            a lot of <a href="https://chatgpt.com/" target="_blank">ChatGPT-4</a>
         <p>&#128027; If you find any bugs, please report! &#128027;<p> 
     </div>
    """, unsafe_allow_html=True)