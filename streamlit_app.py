import streamlit as st
from db.database import init_db
from auth.auth import login_user, register_user
from astrology.kundali import generate_kundali
from astrology.dasha import calculate_vimshottari_dasha
from chatbot.agent import chatbot
from utils.geocode import get_lat_lon
from utils.pdf import generate_pdf
from db.database import save_chat, get_chat_history
from dotenv import load_dotenv
import os

# ---------------- INIT ----------------
init_db()
load_dotenv()

api_key = os.getenv("OPENAI_API_KEY")
db_url = os.getenv("DATABASE_URL")

st.set_page_config(page_title="AI Kundali App", layout="wide")


# ---------------- SESSION STATE ----------------
if "user" not in st.session_state:
    st.session_state.user = None

if "kundali" not in st.session_state:
    st.session_state.kundali = None

if "dasha" not in st.session_state:
    st.session_state.dasha = None

# ---------------- HEADER ----------------
st.title("🔮 AI Kundali & Astrology Advisor")

# ---------------- AUTH ----------------
menu = ["Login", "Register"]

if not st.session_state.user:
    choice = st.sidebar.selectbox("Menu", menu)

    if choice == "Register":
        st.subheader("Create Account")

        username = st.text_input("Username")
        password = st.text_input("Password", type="password")

        if st.button("Register"):
            try:
                register_user(username, password)
                st.success("Account created. Please login.")
            except Exception as e:
                st.error("User may already exist.")

    elif choice == "Login":
        st.subheader("Login")

        username = st.text_input("Username")
        password = st.text_input("Password", type="password")

        if st.button("Login"):
            user = login_user(username, password)

            if user:
                st.session_state.user = user
                st.success("Login successful")
                st.rerun()
            else:
                st.error("Invalid credentials")

# ---------------- MAIN APP ----------------
else:
    st.sidebar.success(f"Logged in as {st.session_state.user.username}")

    if st.sidebar.button("Logout"):
        st.session_state.user = None
        st.rerun()

    tab1, tab2, tab3 = st.tabs(["🔮 Kundali", "💬 Chat", "📄 Download"])

    # ---------------- TAB 1: KUNDALI ----------------
    with tab1:
        st.subheader("Enter Birth Details")

        col1, col2 = st.columns(2)

        with col1:
            dob = st.date_input("Date of Birth")
            tob = st.time_input("Time of Birth")

        with col2:
            place = st.text_input("Place of Birth")

        lat, lon = None, None

        if st.button("📍 Fetch Coordinates"):
            lat, lon = get_lat_lon(place)

            if lat:
                st.success(f"Latitude: {lat}, Longitude: {lon}")
                st.session_state.lat = lat
                st.session_state.lon = lon
            else:
                st.error("Could not fetch location")

        if st.button("✨ Generate Kundali"):
            if "lat" not in st.session_state:
                st.error("Please fetch location first")
            else:
                lat = st.session_state.lat
                lon = st.session_state.lon

                kundali = generate_kundali(str(dob), str(tob), lat, lon)
                dasha = calculate_vimshottari_dasha(str(dob), str(tob))

                st.session_state.kundali = kundali
                st.session_state.dasha = dasha

                st.success("Kundali Generated")

                st.json(kundali)

                st.subheader("🪐 Vimshottari Dasha")
                for d in dasha:
                    st.write(f"{d['planet']}: {d['start']} → {d['end']}")

    # ---------------- TAB 2: CHAT ----------------
    with tab2:
        st.subheader("Ask Astrology Questions")

        if not st.session_state.kundali:
            st.warning("Generate Kundali first")
        else:
            history = get_chat_history(st.session_state.user.id)

            for q, r in history:
                st.chat_message("user").write(q)
                st.chat_message("assistant").write(r)

            user_q = st.chat_input("Ask about marriage, career, health...")

            if user_q:
                with st.spinner("Analyzing your kundali..."):
                    response = chatbot.invoke({
                        "input": user_q,
                        "history": history,
                        "kundali": st.session_state.kundali,
                        "dasha": st.session_state.dasha
                    })

                    answer = response["response"]

                    save_chat(st.session_state.user.id, user_q, answer)

                    st.chat_message("user").write(user_q)
                    st.chat_message("assistant").write(answer)

    # ---------------- TAB 3: PDF ----------------
    with tab3:
        st.subheader("Download Kundali Report")

        if not st.session_state.kundali:
            st.warning("Generate Kundali first")
        else:
            if st.button("📄 Generate PDF"):
                filename = f"{st.session_state.user.username}_kundali.pdf"

                generate_pdf(
                    filename,
                    st.session_state.kundali,
                    st.session_state.dasha
                )

                with open(filename, "rb") as f:
                    st.download_button(
                        "⬇️ Download PDF",
                        f,
                        file_name=filename
                    )

# ---------------- FOOTER ----------------
st.markdown("---")
st.caption("⚠️ This app provides astrology-based insights and should not be considered absolute predictions.")