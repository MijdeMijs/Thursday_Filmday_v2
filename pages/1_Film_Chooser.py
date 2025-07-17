#===============
# Imports
#===============
import streamlit as st
from utils.auth import get_authenticator
import pandas as pd
import time
from datetime import datetime
import gzip
import random
import sqlite3

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

#========================
# Film Chooser intro
#========================

st.header(":clapper: Film Chooser", divider="rainbow")

st.write('''Welcome to the Film Chooser! This is a tool that might help you to choose a 
         movie for the movie night. It is very simple to use, but here are some tips:''')

st.write("""
         **[Search Filters](#search-filters):** When starting the Thursday Filmday app, 
         default filter settings are applied. You can select a main genre and additional 
         genres, or choose **'No preference for any genre...'** to avoid filtering by 
         genre. If you want to filter genres but don't care about the main genre, select 
         **'No preference for a main genre...'**. Be cautious with the votes setting; low 
         settings might exclude good movies. For blockbusters, set a high filter on votes 
         (minimum 200,000).""")

st.write("""
         **[Applied Filters](#applied-filters):** Get a short overview of the filter 
         settings.""")

st.write("""
         **[Possible Movies](#possible-movies):** In this list, you'll find all films that
         match the filter settings you choose. This list will automatically update if you 
         decide to change the filter settings. You'll also see how many films were found 
         and get notified with a warning if you didn't select a genre.""")

st.write("""
         **[Visit IMDb Page](#visit-imdb-page):** With this function, you can easily visit 
         the IMDb film pages of movies that are in the Possible Movies list. Here, you 
         select a subset of films based on a movie's feature that you choose.""")

st.markdown("""
    <style>
    @keyframes rainbow {
        0% {color: red;}
        14% {color: orange;}
        28% {color: yellow;}
        42% {color: green;}
        57% {color: blue;}
        71% {color: indigo;}
        85% {color: violet;}
        100% {color: red;}
    }
    .rainbow-text {
        animation: rainbow 5s infinite;
        font-weight: bold;
    }
    </style>
    <p class="rainbow-text">Good luck chosing your movie!!!</p>
    """, unsafe_allow_html=True)

#=======================
# IMDb data version
#=======================

# Read .txt file with date
with open("utils/film_data_update.txt", "r") as file:
    date_str = file.read().strip()

# Convert text to datetime object
date_film_data = datetime.strptime(date_str, "%d %B %Y")

# Check if year and month are current year and month
if (date_film_data.year == datetime.now().year and
    date_film_data.month == datetime.now().month):

    IMDb_data_version = date_film_data.strftime('%B %d, %Y')
    st.markdown(f'''<span style="font-size: 13px;">*IMDb data version: 
                **{IMDb_data_version}***</span>''', 
                unsafe_allow_html=True)
else:
    IMDb_data_version = date_film_data.strftime('%B %d, %Y')
    st.markdown(f'''<span style="font-size: 13px;">:red[***Notice!** Still using IMDb 
                data version **{IMDb_data_version}**!*]</span>''', 
                unsafe_allow_html=True)
    
#===================
# Movie Filters
#===================

st.subheader('Movie Filters', divider='violet')

st.write('''
        Because some behavior of the Thursday Filmday app drives me up the wall,
        I'll give you two whimsical options for your filters: **(1) forget** your filters
        when you navigate between pages. This will make the filters behave like a well-trained puppy 🐶
        **(2) save** your filters when you navigate between pages. The filters won't reset if you return to the Film Chooser,
        but beware! The filters will act like a mischievous gremlin 😈
	 ''')    

#=================
# Save button
#=================

# Initialize session state if not already done
if 'save_filters' not in st.session_state:
    st.session_state.save_filters = 0

# Toggle button with session state
if st.toggle('Forget/Save', key='toggle', value=st.session_state.save_filters):
    st.session_state.save_filters = 1
else:
    st.session_state.save_filters = 0

save_filters = st.session_state.save_filters

#=====================
# Genre selection
#=====================

st.write('**Genre:**')

#============================
# AND/OR jack in the box
#============================

# Define AND_OR operator
def AND_OR():
    if st.toggle('AND/OR operator'):
        operator = 1
        st.write('''**OR** operator is selected to pass your genres. Notice that this 
                 could give :red[**less precise**], but :red[**more movie options**]!''')
    else:
        operator = 0
        st.write('''**AND** operator is selected to pass your genres. Notice that this 
                 could give :red[**more precise**], but :red[**fewer movie options**]!''')
    return operator

#================
# Genre list
#================    

@st.cache_data
def genre_list():
    conn = sqlite3.connect("data/film_database.db")
    cursor = conn.cursor()

    # Get all column names from film_data
    cursor.execute("PRAGMA table_info(film_data)")
    columns_info = cursor.fetchall()

    # Extract column names
    column_names = [col[1] for col in columns_info]

    # Get columns 7 to 33
    genre_columns = column_names[6:33]

    # Add custom options at the top
    genre_columns.insert(0, "No preference for a main genre...")
    genre_columns.insert(0, "No preference for any genre...")

    conn.close()
    return genre_columns   

# Run genre list
all_genres = genre_list()

# ===============================
# region Main genre
# ===============================

if save_filters == 1:
    if 'selected_main_genre' not in st.session_state:
        st.session_state['selected_main_genre'] = all_genres[0]

    def save_main_genre():
         st.session_state['selected_main_genre'] = st.session_state['key_main_genre']

    main_genre = st.selectbox('Main genre:', all_genres,
                              key='key_main_genre',
                              index=all_genres.index(st.session_state['selected_main_genre']),
                              on_change=save_main_genre)
else:
    main_genre = st.selectbox('Main genre:', all_genres)

#========================
# Genre if-statement
#========================

# Initialize session state
if 'selected_other_genres' not in st.session_state:
    st.session_state['selected_other_genres'] = []

# Define a callback function to update session state
def save_other_genres():
    st.session_state['selected_other_genres'] = st.session_state['key_other_genres']

def process_genre_selection(main_genre, genres, save):
    genre_options = []
    other_genres = []
    genre_selection = []
    operator = 0
    genre_tag = 0

    if main_genre == "No preference for any genre...":
        pass
    else:
        genre_options = [
            genre for genre in genres if genre not in ["No preference for any genre...", 
                                                       "No preference for a main genre..."]
        ]
        if main_genre != "No preference for a main genre...":
            genre_options = [genre for genre in genre_options if genre != main_genre]
            max_genres = 2
            genre_tag = 2
        else:
            max_genres = 3
            genre_tag = 1

        if save == 1:
            other_genres = st.multiselect(
            f"Select a maximum of **{max_genres}** genre(s):",
            options=genre_options,
            default=st.session_state['selected_other_genres'],
            key='key_other_genres',
            on_change=save_other_genres)

            genre_selection = other_genres.copy()
            operator = AND_OR()
        else:
            other_genres = st.multiselect(
            f"Select a maximum of **{max_genres}** genre(s):",
            options=genre_options)

            genre_selection = other_genres.copy()
            operator = AND_OR()

    return genre_options, other_genres, genre_selection, operator, genre_tag

(genre_options, other_genres, 
 genre_selection, operator, 
 genre_tag) = process_genre_selection(main_genre, all_genres, save_filters)

#==================
# Check length
#==================

if genre_tag == 1 and len(genre_selection) > 3:
            st.error("You can select a maximum of 3 genres!")
elif genre_tag == 2 and len(genre_selection) > 2:
            st.error("You can select a maximum of 2 additional genres!")

#=======================================
# Define slider limits and defaults 
#=======================================

@st.cache_data
def dynamic_min_year():
    conn = sqlite3.connect("data/film_database.db")
    cursor = conn.cursor()
    cursor.execute("""
    SELECT
        MIN(startYear)
    FROM film_data
""")
    min_year = cursor.fetchone()[0]
    conn.close()
    return min_year

# year
min_year = dynamic_min_year()
max_year = datetime.now().year
default_min_year = 1985
default_max_year = max_year

# time 
min_time = 30
max_time = 240
default_min_time = 60
default_max_time = 120

# ratings
min_rating = 1.0
max_rating = 10.0
default_min_rating = 7.0
default_max_rating = max_rating
ratings_step_size = 0.5

# votes
min_votes = 0
max_votes = 500000
default_min_votes = 100000
votes_step_size = 500

#====================
# Filter sliders 
#====================

# year slider
st.write('**Year:**')
selected_years = st.slider("Range of years in which a film went into premiere:", 
                   min_year, max_year,
                   (default_min_year, default_max_year),
                   step=1)
st.divider()

# time slider 
st.write('**Duration:**')
selected_time = st.slider("Range of film duration in minutes:", 
                  min_time, max_time,
                  (default_min_time, default_max_time),
                  step=5)
st.divider()

# ratings slider 
st.write('**Rating:**')
selected_rating = st.slider("Range of film IMDb ratings:", 
                    min_value=min_rating,
                    max_value=max_rating,
                    value=(default_min_rating, default_max_rating),
                    step=ratings_step_size,
                    format="%.1f")
st.divider()

# votes slider
st.write('**Votes:**')
selected_votes = st.slider("Minimum number of votes for the IMDb film rating:", 
                   min_votes, max_votes, 
                   default_min_votes,
                   step=votes_step_size)

# =====================
# Film Suggestions
# =====================

st.subheader('Film Suggestions', divider='violet')

#============================
# Define & apply filters
#============================

@st.cache_data
def film_data_filter(selected_years, 
                    selected_time, 
                    selected_rating, 
                    selected_votes,
                    genre_tag, 
                    main_genre, 
                    operator, 
                    genre_selection):

    conn = sqlite3.connect("data/film_database.db")
    cursor = conn.cursor()

    # Start SQL query
    query = """
        SELECT * FROM film_data
        WHERE 
            startYear BETWEEN ? AND ?
            AND runtimeMinutes BETWEEN ? AND ?
            AND averageRating BETWEEN ? AND ?
            AND numVotes >= ?
    """
    params = [
        selected_years[0], selected_years[1],
        selected_time[0], selected_time[1],
        selected_rating[0], selected_rating[1],
        selected_votes
    ]

    # Add main_genre filter if requested
    if genre_tag == 2:
        query += " AND main_genre = ?"
        params.append(main_genre)

    # Add genre column filters
    if genre_tag != 0 and genre_selection:
        if operator == 0:  # AND
            for genre in genre_selection:
                query += f" AND {genre} = 1"
        elif operator == 1:  # OR
            genre_conditions = " OR ".join([f"{genre} = 1" for genre in genre_selection])
            query += f" AND ({genre_conditions})"

    # Run query
    df = pd.read_sql_query(sql=query, con=conn, params=params)
    conn.close()

    return df    

filtered_filma_data = film_data_filter(selected_years, 
                    selected_time, 
                    selected_rating, 
                    selected_votes,
                    genre_tag, 
                    main_genre, 
                    operator, 
                    genre_selection)

#=============================
# Display filtered movies
#=============================

@st.cache_data
def display_filtered_df(filtered_filma_data):
    # Create the DataFrame with selected features and reset the index
    display_df = filtered_filma_data[['tconst', 'primaryTitle', 'startYear', 'runtimeMinutes', 
                              'main_genre', 'other_genres', 'averageRating', 
                              'numVotes']].copy()
    display_df.columns = ['ID', 'Film', 'Year', 'Duration', 'Main genre', 
                          'Additional genres', 'IMDb Rating', 'Number of votes']
    
    # Reset the index and add 1 to start from 1
    display_df.reset_index(drop=True, inplace=True)
    display_df.index = display_df.index + 1
    display_df.index.name = 'Index'

    return display_df

# Run display_filtered_df()
display_df = display_filtered_df(filtered_filma_data)

# Show display_df or error message to user
if (genre_tag == 1 and len(genre_selection) > 3) or (genre_tag == 2 and len(genre_selection) > 2):
    st.error('More than 3 genres are selected!')
elif display_df.empty:
    st.error('No movies found within the boundaries of the chosen filters!')
else:
    st.write(f'Found **{len(display_df)}** films within your chosen filters:')
    st.dataframe(display_df.iloc[:, 1:])            

# ===============================
# region No genre warning
# ===============================

if main_genre in ['No preference for any genre...', 
                  'No preference for a main genre...']:
    if not genre_selection:
        st.markdown(f'''<span style="font-size: 13px;">:red[***Notice!** 
                    No filter was applied on genre!*]</span>''', unsafe_allow_html=True) 
