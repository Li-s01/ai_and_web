import streamlit as st

st.title("Game Statistics")

# Beispielstatistiken aus Session State
rounds_played = st.session_state.get("round", 1) - 1
score = st.session_state.get("score", 0)
accuracy = (score / rounds_played * 100) if rounds_played > 0 else 0

st.write(f"Total Rounds Played: {rounds_played}")
st.write(f"Total Correct Guesses: {score}")
st.write(f"Accuracy: {accuracy:.2f}%")