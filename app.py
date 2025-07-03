import streamlit as st
import requests
import html
import re
import json
import os
from dotenv import load_dotenv

# ------------------- LOAD ENVIRONMENT VARIABLES -------------------
load_dotenv()
HUGGINGFACE_API_KEY = os.getenv("HUGGINGFACE_API_KEY")
OMDB_API_KEY = os.getenv("OMDB_API_KEY")
HF_MODEL = "HuggingFaceH4/zephyr-7b-beta"

# ------------------- STREAMLIT CONFIG -------------------
st.set_page_config(
    page_title="🎬 AI Movie Recommender", page_icon="🎥", layout="centered"
)

st.markdown(
    """
<style>
.stApp {
    background-color: #101418;
    color: #F5F5F5;
    font-family: 'Segoe UI', sans-serif;
}
h1, h2, h3, h4 {
    color: #FF4B4B;
}
.stTextInput>div>div>input, .stSelectbox>div>div, textarea {
    background-color: #1A1D23;
    color: #F5F5F5;
    border: 1px solid #2D2F35;
    border-radius: 5px;
}
.stButton>button {
    background-color: #FF4B4B;
    color: #FFFFFF;
    font-weight: bold;
    border-radius: 8px;
    padding: 0.7rem 1.5rem;
    transition: background-color 0.3s ease;
}
.stButton>button:hover {
    background-color: #E63946;
}
.movie-box {
    background-color: #1E1E1E;
    border-left: 5px solid #FF4B4B;
    padding: 1.5rem;
    border-radius: 10px;
    margin-top: 1.5rem;
    white-space: pre-wrap;
    box-shadow: 0 2px 10px rgba(0,0,0,0.2);
}
</style>
""",
    unsafe_allow_html=True,
)

st.title("🎥 Personality-Based AI Movie Recommender")
st.markdown(
    "Answer a few personality-based questions and get AI-generated movie recommendations!"
)

# ------------------- FORM -------------------
with st.form("movie_form"):
    st.subheader("💬 Tell us about yourself")

    mood = st.text_input(
        "Describe your current mood:", placeholder="e.g., adventurous, nostalgic"
    )
    if not mood:
        mood = st.selectbox(
            "Or pick a mood:",
            ["", "Happy", "Melancholic", "Anxious", "Excited", "Calm"],
        )

    hobby = st.text_input("One hobby you love:", placeholder="e.g., painting, hiking")
    if not hobby:
        hobby = st.selectbox(
            "Or choose a hobby:",
            ["", "Reading", "Traveling", "Gaming", "Cooking", "Photography"],
        )

    genre = st.selectbox(
        "Preferred Genre",
        [
            "Action",
            "Drama",
            "Comedy",
            "Sci-Fi",
            "Romance",
            "Thriller",
            "Mystery",
            "Fantasy",
        ],
    )

    vibe = st.text_input(
        "Pick one word that describes your vibe:",
        placeholder="e.g., bold, chill, curious",
    )
    if not vibe:
        vibe = st.selectbox(
            "Or select a vibe:",
            ["", "Quirky", "Serious", "Dreamy", "Adventurous", "Relaxed"],
        )

    submit = st.form_submit_button("🎬 Recommend Movies")


# ------------------- OMDB FETCH -------------------
def fetch_omdb_info(title):
    try:
        url = f"http://www.omdbapi.com/?apikey={OMDB_API_KEY}&t={requests.utils.quote(title)}"
        res = requests.get(url)
        data = res.json()
        if data.get("Response") == "True":
            return {
                "title": data.get("Title"),
                "year": data.get("Year"),
                "plot": data.get("Plot"),
                "poster": data.get("Poster"),
                "director": data.get("Director"),
            }
    except Exception as e:
        st.error(f"OMDb fetch error: {e}")
    return None


# ------------------- HUGGING FACE REQUEST -------------------
def query_huggingface_model(prompt):
    headers = {
        "Authorization": f"Bearer {HUGGINGFACE_API_KEY}",
        "Content-Type": "application/json",
    }
    payload = {
        "inputs": prompt,
        "parameters": {
            "max_new_tokens": 512,
            "temperature": 0.7,
            "return_full_text": False,
        },
    }
    try:
        response = requests.post(
            f"https://api-inference.huggingface.co/models/{HF_MODEL}",
            headers=headers,
            json=payload,
            timeout=30,
        )
        response.raise_for_status()
        generated = response.json()
        return generated[0].get("generated_text", "") if generated else ""
    except Exception as e:
        st.error(f"❌ Hugging Face API Error: {e}")
        return ""


# ------------------- MAIN LOGIC -------------------
if submit:
    if not mood or not hobby or not vibe:
        st.warning("Please fill in all the fields or pick from the dropdowns.")
    else:
        with st.spinner("✨ AI is generating recommendations..."):
            prompt = f"""
Given the following personality traits:
- Mood: {mood}
- Hobby: {hobby}
- Preferred Genre: {genre}
- Vibe: {vibe}

Suggest 3 to 5 matching movies.

Your response should be ONLY a valid JSON array with each item like:
{{"title": "Movie Title", "reason": "Why it fits"}}
"""
            hf_text = query_huggingface_model(prompt)

            # Try to extract JSON from the model output
            json_match = re.search(r"\[.*\]", hf_text, re.DOTALL)
            if not json_match:
                st.error("❌ The AI response couldn't be parsed.")
                with st.expander("📄 Show raw AI output"):
                    st.code(hf_text)
            else:
                try:
                    suggestions = json.loads(json_match.group(0))
                    if not suggestions:
                        st.warning(
                            "The AI response was empty. Try refining your inputs."
                        )
                    else:
                        st.subheader("🎞️ Your AI Movie Recommendations")
                        for movie in suggestions:
                            title = movie.get("title", "").strip()
                            reason = movie.get("reason", "").strip()
                            if not title or not reason:
                                continue
                            details = fetch_omdb_info(title)
                            if details:
                                st.markdown(
                                    f"""
<div class="movie-box">
    <h4>{details['title']} ({details['year']})</h4>
    <p><strong>Director:</strong> {details.get('director', 'N/A')}</p>
    <p><strong>AI's Reason:</strong> {html.escape(reason)}</p>
    <p><strong>Summary:</strong> {html.escape(details.get('plot', 'N/A'))}</p>
    {'<img src="' + details['poster'] + '" width="180">' if details.get('poster') != 'N/A' else ''}
</div>
""",
                                    unsafe_allow_html=True,
                                )
                            else:
                                st.info(f"🎞️ {title}: {reason} (❌ Not found in OMDb)")
                except json.JSONDecodeError:
                    st.error(
                        "❌ The AI response looked like JSON but couldn't be decoded."
                    )
                    with st.expander("📄 Show raw AI output"):
                        st.code(hf_text)
