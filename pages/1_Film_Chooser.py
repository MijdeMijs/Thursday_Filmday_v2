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
        Set your preferences and discover the perfect movie! 🎥✨ Use the filters 
         to choose your favorite genre 🎭, set your IMDb rating ⭐, and more. 
         Whether you're in the mood for an action-packed thriller or a heartwarming 
         drama, these filters help you find just what you’re looking for!

        👷 Trouble with stuborn filters!? Hit 'em with the wrench 🔧 and turn off 
         *Save filters*. You're a maker!
         ''')    

#=================
# Save toggle
#=================

# Initialize session state if not already done
if 'save_filters2' not in st.session_state:
    st.session_state.save_filters2 = True

# Toggle button with session state
save_toggle = st.toggle("Save filters", key="toggle2", value=st.session_state.save_filters2)
st.session_state.save_filters2 = save_toggle

#=====================
# Genre selection
#=====================

st.write('**Genre:**')

#============================
# AND/OR jack in the box
#============================

def AND_OR():
    # Check if "operator" is in session state, else default to AND (0)
    if 'operator' not in st.session_state:
        st.session_state.operator = 0  # Default to AND

    # Check the toggle state
    if st.toggle('AND/OR operator', key='and_or_toggle', value=st.session_state.operator == 1):
        st.session_state.operator = 1  # OR operator
        st.write('''**OR** operator is selected to pass your genres. Notice that this 
                    could give :red[**less precise**], but :red[**more movie options**]!''')
    else:
        st.session_state.operator = 0  # AND operator
        st.write('''**AND** operator is selected to pass your genres. Notice that this 
                    could give :red[**more precise**], but :red[**fewer movie options**]!''')

    return st.session_state.operator

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

#===============================
# Main genre
#===============================

if save_toggle:
    # Use saved value or default
    default_genre = st.session_state.get("selected_main_genre", all_genres[0])

    # Display selectbox
    main_genre = st.selectbox(
        "Main genre:",
        all_genres,
        index=all_genres.index(default_genre)
    )

    # Save selected genre into session state manually
    st.session_state.selected_main_genre = main_genre

else:
    main_genre = st.selectbox("Main genre:", all_genres)

#========================
# Genre if-statement
#========================

# Only define state if saving is on
if save_toggle and "selected_other_genres" not in st.session_state:
    st.session_state['selected_other_genres'] = []

# Callback to update session state for multiselect
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
            genre for genre in genres if genre not in [
                "No preference for any genre...", 
                "No preference for a main genre..."
            ]
        ]

        if main_genre != "No preference for a main genre...":
            genre_options = [g for g in genre_options if g != main_genre]
            max_genres = 2
            genre_tag = 2
        else:
            max_genres = 3
            genre_tag = 1

        if save:
            other_genres = st.multiselect(
                f"Select a maximum of **{max_genres}** genre(s):",
                options=genre_options,
                default=st.session_state.get('selected_other_genres', []),
                key='key_other_genres',
                on_change=save_other_genres
            )
            genre_selection = other_genres.copy()
            operator = AND_OR()
        else:
            other_genres = st.multiselect(
                f"Select a maximum of **{max_genres}** genre(s):",
                options=genre_options
            )
            genre_selection = other_genres.copy()
            operator = AND_OR()

    return genre_options, other_genres, genre_selection, operator, genre_tag

(genre_options, other_genres, 
 genre_selection, operator, 
 genre_tag) = process_genre_selection(main_genre, all_genres, save_toggle)

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

# === Year Slider ===
st.write('**Year:**')
if save_toggle and "selected_years" in st.session_state:
    default_years = st.session_state.selected_years
else:
    default_years = (default_min_year, default_max_year)

selected_years = st.slider("Range of years in which a film went into premiere:", 
                           min_year, max_year,
                           default_years,
                           step=1)

# Save only if toggle is ON
if save_toggle:
    st.session_state.selected_years = selected_years

st.divider()

# === Duration Slider ===
st.write('**Duration:**')
if save_toggle and "selected_time" in st.session_state:
    default_time = st.session_state.selected_time
else:
    default_time = (default_min_time, default_max_time)

selected_time = st.slider("Range of film duration in minutes:", 
                          min_time, max_time,
                          default_time,
                          step=5)

if save_toggle:
    st.session_state.selected_time = selected_time

st.divider()

# === Rating Slider ===
st.write('**Rating:**')
if save_toggle and "selected_rating" in st.session_state:
    default_rating = st.session_state.selected_rating
else:
    default_rating = (default_min_rating, default_max_rating)

selected_rating = st.slider("Range of film IMDb ratings:", 
                            min_value=min_rating,
                            max_value=max_rating,
                            value=default_rating,
                            step=ratings_step_size,
                            format="%.1f")

if save_toggle:
    st.session_state.selected_rating = selected_rating

st.divider()

# === Votes Slider ===
st.write('**Votes:**')
if save_toggle and "selected_votes" in st.session_state:
    default_votes = st.session_state.selected_votes
else:
    default_votes = default_min_votes

selected_votes = st.slider("Minimum number of votes for the IMDb film rating:", 
                           min_votes, max_votes,
                           default_votes,
                           step=votes_step_size)

if save_toggle:
    st.session_state.selected_votes = selected_votes

#==================
# Reset botton
#==================

# if st.button("🔄 Reset filters"):
#     st.session_state.selected_main_genre = all_genres[0]
#     st.session_state.selected_other_genres = []
#     st.session_state.selected_years = (default_min_year, default_max_year)
#     st.session_state.selected_time = (default_min_time, default_max_time)
#     st.session_state.selected_rating = (default_min_rating, default_max_rating)
#     st.session_state.selected_votes = default_min_votes

#     st.rerun() 

# =====================
# Film Suggestions
# =====================

st.subheader('Film Suggestions', divider='violet')

st.write("""🏴‍☠️ Aye, you've picked your filters, you picky pirate!
         Now, choose how many movie suggestions you want to see, and decide 
         on what treasure (ahem, feature) you want to sort them by! 🏆 Whether 
         it's the highest IMDb rating ⭐ or the longest runtime ⏳, make sure 
         the list fits your legendary taste!
        """)

left_column, right_column = st.columns(2)

with left_column:
    top_n_choice = st.selectbox('Top tier list:', ['Top 100', 
                                                   'Top 250', 
                                                   'Top 500',
                                                   'All'])

    top_n_mapping = {
        'Top 100': 100,
        'Top 250': 250,
        'Top 500': 500,
        'All': None
    }
    top_n = top_n_mapping[top_n_choice]

with right_column:
    # Select on column display_df is sorted
        sort_film_df = st.selectbox("Select a movie feature:", ["IMDb rating", 
                                                                "Year",
                                                                "Duration",
                                                                "Votes"])
        
        sort_mapping = {
            'IMDb rating': 'averageRating',
            'Year': 'startYear',
            'Duration': 'runtimeMinutes',
            'Votes': 'numVotes'
        }
        sort_column = sort_mapping[sort_film_df]

sort_ascending = st.toggle('Descending/ascending', value=False)

st.divider()

#============================
# Define & apply filters
#============================

# @st.cache_data
def film_data_filter(selected_years, 
                     selected_time, 
                     selected_rating, 
                     selected_votes,
                     genre_tag, 
                     main_genre, 
                     operator, 
                     genre_selection,
                     sort_column,
                     top_n):

    conn = sqlite3.connect("data/film_database.db")
    cursor = conn.cursor()

    # Base query
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

    # Optional genre filters
    if genre_tag == 2:
        query += " AND main_genre = ?"
        params.append(main_genre)

    if genre_tag != 0 and genre_selection:
        if operator == 0:  # AND
            for genre in genre_selection:
                query += f" AND {genre} = 1"
        elif operator == 1:  # OR
            genre_conditions = " OR ".join([f"{genre} = 1" for genre in genre_selection])
            query += f" AND ({genre_conditions})"

    # Add ORDER BY and LIMIT
    order = "ASC" if sort_ascending else "DESC"
    query += f" ORDER BY {sort_column} {order}"

    if top_n is not None:
        query += " LIMIT ?"
        params.append(top_n)

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
                                       genre_selection,
                                       sort_column,
                                       top_n)

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
    st.write(f'Behold! **{len(display_df)}** films that are within your chosen filters:')
    st.dataframe(display_df.iloc[:, 1:])            

# ===============================
# region No genre warning
# ===============================

if main_genre in ['No preference for any genre...', 
                  'No preference for a main genre...']:
    if not genre_selection:
        st.markdown(f'''<span style="font-size: 13px;">:red[***Notice!** 
                    No filter was applied on genre!*]</span>''', unsafe_allow_html=True) 

#=====================
# Visit IMDb page
#=====================

st.divider()

st.write("""🕵️‍♂️ Elementary, my dear cinephile...

You have a list of suspects—I mean, *films*. But the clues don’t end here. 
         For further investigation, I suggest heading to the scene of 
         the crime: **IMDb**

After all, every great mystery deserves a closer look... 🧐🔍

""")

# Select a movie
IMDb_link = st.selectbox("Select film:", display_df['Film'].unique())
            
# Get film ID
ID = display_df[display_df['Film'] == IMDb_link].iloc[0, 0]

# Define IMDb URL
url = f'https://www.imdb.com/title/{ID}/'

# Link button in first column
st.link_button("Visit IMDb page!", url)

#==================
# End the pain
#==================

st.divider()

st.write("""Did your movie selection turn out to be just as hopeless as your 
         thesis ☠️!? Don't worry, it'll be over soon... Press the button 🥀⚰️ and
         pick a random film within your movie preferences.""")

if st.button('END THE PAIN 💉'):
    end_pain = display_df.sample(1)

    # Extract values from the row
    film_title = end_pain['Film'].values[0]
    film_year = end_pain['Year'].values[0]
    rating = end_pain['IMDb Rating'].values[0]

    # Display the film suggestion
    st.write(f"💊 You must watch **{film_title}** ({film_year}) — IMDb {rating}/10")


# ===========
# Footer
# ===========

st.divider()

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
            so long to choose a movie that he developed a movie app in the 
            meantime - <a href="https://eelslap.com/" target="_blank">ADHD hyperfocus</a> - 
            <a href="https://streamlit.io/" target="_blank">Streamlit</a> - 
            <a href="https://developer.imdb.com/" target="_blank">IMDb Developer</a> and
            a lot of <a href="https://chatgpt.com/" target="_blank">ChatGPT-4</a>
         <p>&#128027; If you find any bugs, please report! &#128027;<p> 
     </div>
    """, unsafe_allow_html=True)
