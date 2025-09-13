---
title: Personality AI Recommender
emoji: 🧠
colorFrom: indigo
colorTo: purple
sdk: streamlit
app_file: app.py
pinned: false
---

# 🧠 Personality-based AI Recommender

Tired of the same old recommendations creating a filter bubble? This project is an innovative recommender system that suggests movies, books, and travel destinations based on a user's intrinsic **personality traits**, moving beyond traditional metrics like viewing history.

The goal is to provide novel, diverse, and genuinely personalized recommendations that encourage discovery by aligning with a user's core character, as determined by the scientifically-backed **Big Five (OCEAN)** personality model.

## ✨ Key Features

* **📝 Interactive Personality Quiz:** A short, engaging quiz for users to determine their Big Five (Openness, Conscientiousness, Extraversion, Agreeableness, Neuroticism) profile.
* **🤖 LLM-Powered Recommendations:** Leverages a powerful Large Language Model to generate creative and suitable recommendations that go beyond simple database lookups.
* **💬 Personalized Explanations:** The AI doesn't just recommend an item; it explains **why** that item is a good match for the user's specific personality (e.g., "As someone high in Openness, you would likely enjoy the complex world-building of 'Dune'").
* **🌍 Multi-Domain Suggestions:** The system is designed to provide recommendations across different categories, including movies, books, and travel destinations.



## How It Works

The application follows a simple yet powerful workflow:
1.  **Personality Quiz:** The user answers a series of questions to gauge their personality.
2.  **Profile Generation:** The system calculates the user's Big Five (OCEAN) scores.
3.  **Dynamic Prompt Engineering:** A detailed prompt is constructed that describes the user's personality profile and requests tailored recommendations.
4.  **LLM Inference:** The prompt is sent to a powerful LLM (e.g., Groq, Gemini) via an API.
5.  **Display Results:** The LLM's response, containing the recommendations and their justifications, is parsed and displayed to the user in a clean and interactive UI.

## 🛠️ Technology Stack

* **Frontend & UI:** Streamlit
* **AI Frameworks:** HuggingFace (for prompt management and chaining)
* **LLM:** Zephyr Model
* **Core Logic:** Python
* **Data Handling:** Pandas

## 🚀 How to Run Locally

1.  **Clone the Repository:**
    ```bash
    git clone [https://your-repo-url.git](https://your-repo-url.git)
    cd personality-recommender
    ```

2.  **Install Dependencies:**
    This project uses Poetry for dependency management.
    ```bash
    poetry install
    ```

3.  **Configure Environment:**
    * Create a `.env` file in the project root.
    * Add your LLM API key: `GROQ_API_KEY="your_api_key_here"`

4.  **Run the Streamlit App:**
    ```bash
    poetry run streamlit run app.py
    ```
