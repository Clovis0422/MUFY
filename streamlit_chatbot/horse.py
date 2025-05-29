import streamlit as st
import random
import time

st.set_page_config(page_title="Emoji Horse Race Game", layout="wide")

# Setup
track_length = 20
players = {
    "🐎1": 0,
    "🐎2": 0,
    "🐎3": 0,
    "🐎4": 0,
    "🐎5": 0
}

if "positions" not in st.session_state:
    st.session_state.positions = players.copy()
    st.session_state.winner = None
    st.session_state.race_in_progress = False
    st.session_state.scores = {emoji: 0 for emoji in players}
    st.session_state.bet = None

st.title("🐎🏁 Emoji Horse Race Game")

left_col, right_col = st.columns([3, 1])

with right_col:
    # Betting
    st.subheader("💰 Place Your Bet")
    st.session_state.bet = st.radio("Which horse do you think will win?", list(players.keys()), index=0)

    # Scoreboard
    st.subheader("📊 Scoreboard")
    scoreboard_df = st.session_state.scores
    for horse, score in scoreboard_df.items():
        st.write(f"{horse}: {score} wins")

# Race logic and display
race_placeholder = left_col.empty()
def display_race():
    with race_placeholder.container():
        for emoji, pos in st.session_state.positions.items():
            track = "🏁" + "⬜" * pos + emoji + "⬜" * (track_length - pos)
            st.write(track)

if st.session_state.race_in_progress:
    while not st.session_state.winner:
        for emoji in st.session_state.positions:
            if st.session_state.positions[emoji] < track_length:
                st.session_state.positions[emoji] += random.randint(1, 3)
                if st.session_state.positions[emoji] >= track_length:
                    st.session_state.positions[emoji] = track_length
                    st.session_state.winner = emoji
                    st.session_state.scores[emoji] += 1
                    break
        display_race()
        time.sleep(0.5)
    st.session_state.race_in_progress = False

# Show race track when no race in progress
if not st.session_state.race_in_progress:
    display_race()

# Race button
if st.button("🎲 Race!"):
    if not st.session_state.winner:
        st.session_state.race_in_progress = True
        st.rerun()

# Show winner and betting result
if st.session_state.winner:
    st.success(f"🏆 {st.session_state.winner} wins the race!")
    if st.session_state.bet == st.session_state.winner:
        st.balloons()
        st.success("🎉 Congratulations! You guessed correctly!")
    else:
        st.error("😢 Sorry, your bet didn't win this time.")

# Restart
restart_clicked = st.button("🔄 Restart")
if restart_clicked:
    st.session_state.positions = players.copy()
    st.session_state.winner = None
    st.session_state.race_in_progress = False
    st.rerun()