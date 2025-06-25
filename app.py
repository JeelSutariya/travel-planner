import streamlit as st
import random
from datetime import date

# Sample data for destinations, places, and transport
DESTINATIONS = [
    {
        "name": "Paris",
        "mood": ["romantic", "artsy", "foodie"],
        "places": ["Eiffel Tower", "Louvre Museum", "Montmartre"],
        "transport": ["Metro", "Bicycle", "Walking"]
    },
    {
        "name": "Tokyo",
        "mood": ["techy", "adventurous", "foodie"],
        "places": ["Shibuya Crossing", "Akihabara", "Tsukiji Market"],
        "transport": ["Subway", "Bullet Train", "Taxi"]
    },
    {
        "name": "Rome",
        "mood": ["historic", "romantic", "foodie"],
        "places": ["Colosseum", "Vatican City", "Trevi Fountain"],
        "transport": ["Bus", "Scooter", "Walking"]
    },
    {
        "name": "Sydney",
        "mood": ["adventurous", "beachy", "chill"],
        "places": ["Opera House", "Bondi Beach", "Harbour Bridge"],
        "transport": ["Ferry", "Train", "Bus"]
    },
    {
        "name": "New York",
        "mood": ["urban", "artsy", "foodie"],
        "places": ["Central Park", "MoMA", "Times Square"],
        "transport": ["Subway", "Taxi", "Walking"]
    },
    {
        "name": "Reykjavik",
        "mood": ["nature", "chill", "adventurous"],
        "places": ["Blue Lagoon", "Golden Circle", "Hallgrimskirkja"],
        "transport": ["Bus", "Car Rental", "Walking"]
    },
]

# Playful quiz questions
QUIZ = [
    {
        "question": "What are you in the mood for today?",
        "options": [
            ("Romance and candlelight", "romantic"),
            ("Epic food adventures", "foodie"),
            ("History and old stones", "historic"),
            ("Tech and neon lights", "techy"),
            ("Chilling by the beach", "beachy"),
            ("Nature and wild places", "nature"),
            ("Urban jungle fun", "urban"),
            ("Art and museums", "artsy"),
            ("Adrenaline and adventure", "adventurous"),
            ("Just want to relax", "chill")
        ]
    }
]

def playful_header():
    st.title("🌴 Holiday Genie: Your Playful Trip Booker!")
    st.write("Hello, wanderluster! Ready to let fate (and a little AI magic) pick your next adventure?")

def quiz():
    st.header("🧞‍♂️ Let's start with a quick mood quiz!")
    mood = None
    for q in QUIZ:
        option_labels = [opt[0] for opt in q["options"]]
        choice = st.radio(q["question"], option_labels)
        for label, mood_val in q["options"]:
            if choice == label:
                mood = mood_val
    return mood

def suggest_destinations(mood):
    filtered = [d for d in DESTINATIONS if mood in d["mood"]]
    if len(filtered) < 5:
        # Fill up with randoms if not enough
        others = [d for d in DESTINATIONS if d not in filtered]
        filtered += random.sample(others, min(5 - len(filtered), len(others)))
    else:
        filtered = random.sample(filtered, 5)
    return filtered

def main():
    playful_header()
    if "step" not in st.session_state:
        st.session_state.step = 0
    if "mood" not in st.session_state:
        st.session_state.mood = None
    if "destination" not in st.session_state:
        st.session_state.destination = None
    if "date" not in st.session_state:
        st.session_state.date = None
    if "budget" not in st.session_state:
        st.session_state.budget = None
    if "days" not in st.session_state:
        st.session_state.days = None

    if st.session_state.step == 0:
        mood = quiz()
        if st.button("Show me my dream destinations!"):
            st.session_state.mood = mood
            st.session_state.step = 1
            st.rerun()

    elif st.session_state.step == 1:
        st.header("✨ Here are 5 magical places for you!")
        suggestions = suggest_destinations(st.session_state.mood)
        dest_names = [d["name"] for d in suggestions]
        dest_choice = st.radio("Which one makes your heart skip a beat?", dest_names)
        if st.button("That's the one!"):
            st.session_state.destination = dest_choice
            st.session_state.step = 2
            st.rerun()

    elif st.session_state.step == 2:
        st.header(f"🗓️ Let's plan your trip to {st.session_state.destination}!")
        trip_date = st.date_input("When do you want to start your adventure?", min_value=date.today())
        budget = st.number_input("What's your budget in $ (be honest, the Genie won't judge!)", min_value=100, step=50)
        if st.button("Next: Trip Duration"):
            st.session_state.date = trip_date
            st.session_state.budget = budget
            st.session_state.step = 3
            st.rerun()

    elif st.session_state.step == 3:
        st.header(f"⏳ How many days will you explore {st.session_state.destination}?")
        days = st.slider("Number of days", 1, 21, 5)
        if st.button("Show me the magic!"):
            st.session_state.days = days
            st.session_state.step = 4
            st.rerun()

    elif st.session_state.step == 4:
        dest = next(d for d in DESTINATIONS if d["name"] == st.session_state.destination)
        st.header(f"🎉 Your {st.session_state.days}-day adventure in {dest['name']}!")
        st.write(f"**Must-see places:** ")
        for place in dest["places"]:
            st.write(f"- {place}")
        st.write(f"**Getting around:** ")
        st.write(", ".join(dest["transport"]))
        st.success("Ready to book? (Well, this is just a demo Genie, but you can start packing!)")
        if st.button("Start Over"):
            for key in ["step", "mood", "destination", "date", "budget", "days"]:
                st.session_state[key] = None
            st.session_state.step = 0
            st.rerun()

if __name__ == "__main__":
    main()