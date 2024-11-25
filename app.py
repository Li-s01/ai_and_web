import streamlit as st
import random
import pandas as pd

# Lade CSV-Datei
data = pd.read_csv("countries.csv")

# Session State initialisieren
if "random_country" not in st.session_state:
    st.session_state.random_country = None
if "hints" not in st.session_state:
    st.session_state.hints = []
if "hint_count" not in st.session_state:
    st.session_state.hint_count = 0
if "messages" not in st.session_state:  
    st.session_state.messages = []
if "score" not in st.session_state:
    st.session_state.score = 0
if "round" not in st.session_state:
    st.session_state.round = 1
if "game_over" not in st.session_state:
    st.session_state.game_over = False
if "play_next_round" not in st.session_state:
    st.session_state.play_next_round = False  # Flag für neue Runde

# Titel
st.title("Country Guessing Game")
st.write(f"Score: {st.session_state.score}")

# Neue Runde initialisieren
if st.session_state.random_country is None:
    if not st.session_state.play_next_round:  # Nur, wenn nicht bereits auf "Yes" geklickt wurde
        # Runde anzeigen
        round_message = f"**Round {st.session_state.round}**"
        st.session_state.messages.append({"role": "assistant", "content": round_message})
        
        # Neues Land auswählen
        st.session_state.number = random.randint(1, len(data) - 1)
        st.session_state.random_country = data.loc[st.session_state.number, "name"]
        st.session_state.hints = [
            f"The country is on the continent {data.loc[st.session_state.number, 'region']}.",
            f"The country uses the currency {data.loc[st.session_state.number, 'currency']}.",
            f"The capital of the country is '{data.loc[st.session_state.number, 'capital']}'.",
            f"The country has the flag {data.loc[st.session_state.number, 'emoji']}.",
            f"The official country code is {data.loc[st.session_state.number, 'iso3']}.",
            f"The country starts with the letters {data.loc[st.session_state.number, 'name'][:2]}'."
        ]
        st.session_state.hint_count = 0
        st.session_state.game_over = False  # Spiel ist aktiv
        st.session_state.play_next_round = True  # Runde aktivieren
        
        # Ersten Hint hinzufügen
        st.session_state.messages.append({"role": "assistant", "content": st.session_state.hints[0]})

# Chat-Verlauf anzeigen
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])

# Benutzerinput, falls die Runde nicht beendet ist
if not st.session_state.game_over:
    user_input = st.chat_input("Guess a country")
    if user_input:  # Wenn der Benutzer etwas eingibt
        user_input = user_input.strip().lower()
        st.session_state.messages.append({"role": "user", "content": user_input})
        with st.chat_message("user"):
            st.write(user_input)

        # Prüfung der Antwort
        if user_input == st.session_state.random_country.strip().lower():
            # Richtige Antwort
            feedback = f"✅ Correct! The country is {st.session_state.random_country}."
            st.session_state.score += 1
            st.session_state.game_over = True
            st.session_state.messages.append({"role": "assistant", "content": feedback})
            with st.chat_message("assistant"):
                st.write(feedback)
        else:
            # Falsche Antwort
            st.session_state.hint_count += 1
            if st.session_state.hint_count < len(st.session_state.hints):
                # Nächsten Hint anzeigen
                feedback = f"❌ Wrong! Try again.\n\nHint: {st.session_state.hints[st.session_state.hint_count]}"
            else:
                # Alle Hints aufgebraucht
                feedback = f"❌ Wrong! No more hints available. The correct answer was: {st.session_state.random_country}."
                st.session_state.game_over = True

            st.session_state.messages.append({"role": "assistant", "content": feedback})
            with st.chat_message("assistant"):
                st.write(feedback)

# Frage nach neuer Runde, wenn das Spiel vorbei ist
if st.session_state.game_over:
    question = f"Your score:{st.session_state.score}\n\n Do you want to play the next round?"
    st.session_state.messages.append({"role": "assistant", "content": question})
    with st.chat_message("assistant"):
        st.write(question)

    col1, col2 = st.columns(2)  # Zwei Buttons nebeneinander
    with col1:
        if st.button("Yes"):
            # Neues Spiel starten
            st.session_state.random_country = None
            st.session_state.round += 1
            st.session_state.play_next_round = False  # Reset für nächste Runde
             # Seite neu laden, um neue Runde zu starten
    with col2:
        if st.button("No"):
            # Spiel beenden
            goodbye_message = "Thanks for playing! See you next time!"
            st.session_state.messages.append({"role": "assistant", "content": goodbye_message})
            with st.chat_message("assistant"):
                st.write(goodbye_message)

#Man muss zweimal auf yes button drücken!
