import streamlit as st
import random

# Constants
MAX_HP = 4
MAX_ITEMS = 2
ITEMS = ["🧋 Boba", "🔗 Handcuffs", "🔥 Lighter"]

# Initialize session state
if 'players' not in st.session_state:
    st.session_state.players = []
if 'turn_index' not in st.session_state:
    st.session_state.turn_index = 0
if 'game_started' not in st.session_state:
    st.session_state.game_started = False
if 'turn_order' not in st.session_state:
    st.session_state.turn_order = []
if 'game_log' not in st.session_state:
    st.session_state.game_log = []
if 'item_given_this_turn' not in st.session_state:
    st.session_state.item_given_this_turn = False
if 'lighter_active' not in st.session_state:
    st.session_state.lighter_active = {}

# Utility
def add_log(msg):
    st.session_state.game_log.insert(0, msg)

def get_random_item():
    return random.choice(ITEMS)

def use_item(player, item_name, target_index=None):
    if item_name == "🧋 Boba":
        if player['hp'] < MAX_HP:
            player['hp'] += 1
            player['items'].remove("🧋 Boba")
            add_log(f"{player['name']} drank Boba 🧋 and healed +1 HP!")
        else:
            st.info("You already have full HP.")
    elif item_name == "🔗 Handcuffs":
        if target_index is not None:
            player['items'].remove("🔗 Handcuffs")
            st.session_state.players[target_index]['skip'] = True
            add_log(f"{player['name']} used 🔗 Handcuffs on {st.session_state.players[target_index]['name']}!")
    elif item_name == "🔥 Lighter":
        if not st.session_state.lighter_active.get(player['name'], False):
            player['items'].remove("🔥 Lighter")
            st.session_state.lighter_active[player['name']] = True
            add_log(f"{player['name']} used 🔥 Lighter! The next shot deals double damage.")
        else:
            st.info("Lighter already active this turn!")

def display_hearts(hp):
    return "❤️" * hp + "🖤" * (MAX_HP - hp)

# Setup screen
if not st.session_state.game_started:
    st.title("Russian Roulette")
    st.subheader("Spin. Shoot. Survive.")
    num_players = st.slider("Choose number of players", 2, 4)
    player_names = []

    for i in range(num_players):
        name = st.text_input(f"Player {i + 1} Name", f"Player {i + 1}")
        player_names.append(name)

    if st.button("Start Game"):
        st.session_state.players = [{
            "name": name,
            "hp": MAX_HP,
            "items": [],
            "skip": False
        } for name in player_names]
        st.session_state.turn_order = list(range(num_players))
        st.session_state.turn_index = 0
        st.session_state.game_log = []
        st.session_state.item_given_this_turn = False
        st.session_state.lighter_active = {}
        st.session_state.game_started = True
        st.rerun()

# Game Loop
if st.session_state.game_started:
    players = st.session_state.players
    turn_order = st.session_state.turn_order
    turn_index = st.session_state.turn_index

    st.sidebar.markdown("### 📘 Item Guide")
    st.sidebar.markdown("""
- 🧋 **Boba**: +1 HP (can't exceed max HP).
- 🔗 **Handcuffs**: Skip another player’s next turn.
- 🔥 **Lighter**: Next bullet deals 2 damage (only 1 use per turn).
    """)

    # Player status
    st.subheader("📋 Player Status")
    st.table({
        "Name": [p["name"] for p in players],
        "HP ❤️": [display_hearts(p["hp"]) for p in players],
        "Items 🎒": [", ".join(p["items"]) if p["items"] else "-" for p in players]
    })

    # Win check
    if len(players) == 1:
        st.success(f"🏆 {players[0]['name']} wins!")
        st.balloons()
        st.session_state.game_started = False
        st.stop()

    current_player_index = turn_order[turn_index % len(turn_order)]
    player = players[current_player_index]

    # Skip check
    if player['skip']:
        st.warning(f"{player['name']} is handcuffed 🔗 and skips their turn.")
        player['skip'] = False
        st.session_state.turn_index += 1
        st.session_state.item_given_this_turn = False
        st.session_state.lighter_active[player['name']] = False
        add_log(f"{player['name']} was skipped due to handcuffs.")
        st.rerun()

    st.markdown(f"## 🎯 {player['name']}'s Turn")
    st.markdown(f"**HP:** {display_hearts(player['hp'])} | **Items:** {', '.join(player['items']) if player['items'] else 'None'}")

    # Give item
    if not st.session_state.item_given_this_turn and len(player['items']) < MAX_ITEMS:
        new_item = get_random_item()
        player['items'].append(new_item)
        add_log(f"{player['name']} received {new_item}.")
        st.session_state.item_given_this_turn = True

    # Use item
    for idx, item in enumerate(player['items']):
        if item == "🧋 Boba":
            if player['hp'] < MAX_HP:
                if st.button("🧋 Drink Boba", key=f"boba_{idx}"):
                    use_item(player, item)
                    st.rerun()
            else:
                st.button("🧋 Full HP", key=f"boba_disabled_{idx}", disabled=True)

        elif item == "🔗 Handcuffs":
            options = [p["name"] for i, p in enumerate(players) if i != current_player_index]
            if options:
                target_name = st.selectbox("🔗 Choose target", options, key=f"cuff_target_{idx}")
                target_idx = next(i for i, p in enumerate(players) if p["name"] == target_name)
                if st.button("🔗 Use Handcuffs", key=f"handcuffs_{idx}"):
                    use_item(player, item, target_idx)
                    st.rerun()

        elif item == "🔥 Lighter":
            if st.button("🔥 Use Lighter", key=f"lighter_{idx}"):
                use_item(player, item)
                st.rerun()

    # Shooting Phase
    st.markdown("### 💥 Shoot someone")
    targets = [p["name"] for i, p in enumerate(players)]
    target_choice = st.selectbox("Choose who to shoot", targets, key="shoot_choice")
    target_idx = next(i for i, p in enumerate(players) if p["name"] == target_choice)

    if st.button("🔫 Pull the Trigger"):
        bullet_fires = random.randint(1, 2) == 1
        damage = 2 if st.session_state.lighter_active.get(player['name'], False) else 1

        if bullet_fires:
            players[target_idx]["hp"] -= damage
            st.session_state.lighter_active[player['name']] = False
            hit_msg = f"💥 {players[target_idx]['name']} got hit for {damage} damage!"
            st.error(hit_msg)
            add_log(hit_msg)

            if players[target_idx]["hp"] <= 0:
                out_msg = f"💀 {players[target_idx]['name']} is eliminated!"
                st.error(out_msg)
                add_log(out_msg)
                players.pop(target_idx)
                st.session_state.turn_order = [
                    i if i < target_idx else i - 1
                    for i in st.session_state.turn_order if i != target_idx
                ]
                if st.session_state.turn_index >= len(st.session_state.turn_order):
                    st.session_state.turn_index = 0
                st.session_state.item_given_this_turn = False
                st.rerun()
        else:
            st.success("Click! The chamber was empty.")
            add_log(f"{player['name']} pulled the trigger on {target_choice}, but it was a blank.")

        st.session_state.turn_index += 1
        st.session_state.item_given_this_turn = False
        st.session_state.lighter_active[player['name']] = False
        st.rerun()

    # Game Log
    st.markdown("### 📜 Game Log (most recent on top)")
    for line in st.session_state.game_log[:10]:
        st.write(line)