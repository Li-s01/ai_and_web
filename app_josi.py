
import streamlit as st
import pandas as pd
import numpy as np

# Load the countries dataset
@st.cache_data
def load_data():
    return pd.read_csv("countries.csv")

df = load_data()

# Initialize session state for tracking
if 'goal' not in st.session_state:
    st.session_state.goal = df.sample(1)['name'].values[0]

if 'counter' not in st.session_state:
    st.session_state.counter = 0

if 'game_stats' not in st.session_state:
    st.session_state.game_stats = []

if 'messages' not in st.session_state:
    st.session_state.messages = [{"role": "system", "content": "Let's play a guessing game! Guess the country."}]

# Define reset function for a new game
def reset_game():
    st.session_state.goal = df.sample(1)['name'].values[0]
    st.session_state.counter = 0
    st.session_state.messages = [{"role": "system", "content": "New game started! Guess the country."}]

# Sidebar for navigation
st.sidebar.title("Navigation")
page = st.sidebar.radio("Go to", ["Play", "Stats"])

# Play page
if page == "Play":
    st.title("Guess the Country Game")

    # Display chat messages
    for msg in st.session_state.messages:
        if msg["role"] == "system":
            st.markdown(f"**System**: {msg['content']}")
        else:
            st.markdown(f"**You**: {msg['content']}")

    # Input box for user guess
    user_input = st.text_input("Your guess:", key="guess_input")
    if st.button("Submit"):
        if user_input:
            st.session_state.counter += 1
            if user_input.lower() == st.session_state.goal.lower():
                st.session_state.messages.append({"role": "user", "content": user_input})
                st.session_state.messages.append(
                    {"role": "system", "content": f"Correct! The country was {st.session_state.goal}. You guessed it in {st.session_state.counter} tries."}
                )
                st.session_state.game_stats.append(st.session_state.counter)
                reset_game()
            else:
                hint = "Try again!"  
                st.session_state.messages.append({"role": "user", "content": user_input})
                st.session_state.messages.append({"role": "system", "content": hint})

    if st.button("Restart Game"):
        reset_game()

# Stats page
elif page == "Stats":
    st.title("Game Stats")
    total_games = len(st.session_state.game_stats)
    st.write(f"Total games played: {total_games}")

    if total_games > 0:
        avg_guesses = np.mean(st.session_state.game_stats)
        st.write(f"Average number of guesses per game: {avg_guesses:.2f}")

        # Bar chart of guesses per game
        st.bar_chart(pd.DataFrame({"Game": range(1, total_games + 1), "Guesses": st.session_state.game_stats}).set_index("Game"))
    else:
        st.write("No games played yet.")



# Define hints as a list of messages
hints = [
    f"1) The country is on this continent: {region[num]}",
    f"2) More specifically: {subregion[num]}",
    f"3) {capital[num]} is the capital of this country.",
    f"4) Maybe this will help: in the country, people are paying with {currency[num]}",
    f"5) Last tip: in short, the code for the wanted country is {code[num]}"
]

# Loop through the hints and display them based on the counter
for i in range(st.session_state.counter):
    st.write(hints[i])