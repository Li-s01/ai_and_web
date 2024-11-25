import streamlit as st
import random
import pandas as pd
#, key="user_input"
# load csv file
data = pd.read_csv("countries.csv")

# st.session_states for random country and the feedback
if "random_country" not in st.session_state:
    st.session_state.random_country = None
if "number" not in st.session_state:
    st.session_state.number = None
if "feedback" not in st.session_state:
    st.session_state.feedback = ""

# Title
st.title("Capital Guessing Game")

# Select random country after clicking button
if st.button("Guess a capital"):
    st.session_state.number = random.randint(1, 247)
    st.session_state.random_country = data.loc[st.session_state.number, "name"]
    st.session_state.correct_capital= data.koc[st.session_state.number, "capital"]
    st.session_state.feedback = ""  # Feedback zurücksetzen

# Frage und Antwort
#if st.session_state.random_country is not None:
    #country_name = st.session_state.random_country["name"]
    #correct_capital = st.session_state.random_country["capital"]

    user_input = st.text_input(f"What is the capital city of {st.session_state.random_country}?", key="user_input")

    if st.button("Submit"):
        if user_input.strip().lower() == st.session_state.correct_capital.strip().lower():
            st.session_state.feedback = f"✅ Correct! The capital of {st.session_state.random_country} is {st.session_state.correct_capital}."
        else:
            st.session_state.feedback = f"❌ Wrong! The capital of {st.session_state.random_country} is {st.session_state.correct_capital}."

# shows Feedback
if st.session_state.feedback:
    st.write(st.session_state.feedback)
    if st.button("New country"): #Problem: muss man zweimal drücken
        st.session_state.number = random.randint(1, 247)
        st.session_state.random_country = data.loc[st.session_state.number, "name"]
        st.session_state.feedback = "" 
    
