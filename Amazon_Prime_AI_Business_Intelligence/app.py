import streamlit as st
import pandas as pd
import os
import sys
from pathlib import Path

from dotenv import load_dotenv
from google import genai


# ==========================================
# 1. PROJECT PATH AND IMPORTS
# ==========================================

BASE_DIR = Path(__file__).resolve().parent

sys.path.insert(0, str(BASE_DIR))

from src.data_processing import load_and_clean_data


# ==========================================
# 2. PAGE CONFIGURATION
# ==========================================

st.set_page_config(
    page_title="Amazon Prime AI Assistant",
    page_icon="🎬",
    layout="wide"
)

st.title("🎬 Amazon Prime AI Business Intelligence Assistant")

st.markdown("""
<style>

/* Main dashboard background */
[data-testid="stAppViewContainer"] {
    background-color: #F4F7FB !important;
}

/* Header background */
[data-testid="stHeader"] {
    background-color: #F4F7FB !important;
}

/* Sidebar background */
[data-testid="stSidebar"] {
    background-color: #172B4D !important;
}

/* Sidebar text */
[data-testid="stSidebar"] p,
[data-testid="stSidebar"] span,
[data-testid="stSidebar"] label {
    color: white !important;
}

/* Main headings */
h1, h2, h3 {
    color: #172B4D !important;
}

/* Metric cards */
[data-testid="stMetric"] {
    background-color: white !important;
    padding: 18px !important;
    border-radius: 12px !important;
    border: 1px solid #E0E6EF !important;
}

</style>
""", unsafe_allow_html=True)


# ==========================================
# 3. LOAD GEMINI API
# ==========================================

load_dotenv(BASE_DIR / ".env")

API_KEY = os.getenv("GEMINI_API_KEY")

if not API_KEY:

    st.error(
        "Gemini API key not found. Please check your .env file."
    )

    st.stop()

client = genai.Client(api_key=API_KEY)


# ==========================================
# 4. LOAD CLEANED DATASETS
# ==========================================

@st.cache_data
def load_data():

    return load_and_clean_data()


try:

    titles, credits = load_data()

    st.success("Cleaned datasets loaded successfully!")

except Exception as e:

    st.error(f"Unable to load datasets: {e}")

    st.stop()


# ==========================================
# 5. CALCULATE BUSINESS METRICS
# ==========================================

total_titles = len(titles)

total_credits = len(credits)

total_movies = (titles["type"] == "MOVIE").sum()

total_shows = (titles["type"] == "SHOW").sum()

average_imdb = titles["imdb_score"].mean()

average_tmdb = titles["tmdb_score"].mean()

top_genres = (
    titles["genres"]
    .explode()
    .dropna()
    .value_counts()
    .head(10)
)

top_countries = (
    titles["production_countries"]
    .explode()
    .dropna()
    .value_counts()
    .head(10)
)

yearly_content = (
    titles.groupby("release_year")
    .size()
    .sort_index()
)

oldest_year = titles["release_year"].min()

latest_year = titles["release_year"].max()


# ==========================================
# 6. DASHBOARD METRICS
# ==========================================

st.subheader("📊 Dataset Overview")

col1, col2, col3, col4 = st.columns(4)

col1.metric(
    "Total Titles",
    f"{total_titles:,}"
)

col2.metric(
    "Total Movies",
    f"{total_movies:,}"
)

col3.metric(
    "Total TV Shows",
    f"{total_shows:,}"
)

col4.metric(
    "Average IMDb Rating",
    f"{average_imdb:.2f}"
)


st.divider()


# ==========================================
# 7. ADDITIONAL DATASET INFORMATION
# ==========================================

st.subheader("📁 Dataset Information")

info_col1, info_col2, info_col3 = st.columns(3)

info_col1.metric(
    "Total Credits Records",
    f"{total_credits:,}"
)

info_col2.metric(
    "Average TMDB Rating",
    f"{average_tmdb:.2f}"
)

info_col3.metric(
    "Release Year Range",
    f"{oldest_year} - {latest_year}"
)


st.divider()


# ==========================================
# 8. CONTENT ANALYSIS
# ==========================================

left, right = st.columns(2)

with left:

    st.subheader("🎭 Top 10 Genres")

    st.bar_chart(top_genres)


with right:

    st.subheader("🌍 Top 10 Production Countries")

    st.bar_chart(top_countries)


st.subheader("📅 Content by Release Year")

st.line_chart(yearly_content)


st.divider()


# ==========================================
# 9. PREPARE DATA CONTEXT FOR GEMINI
# ==========================================

data_context = f"""

You are analysing an Amazon Prime content catalogue dataset.

DATASET OVERVIEW:

Total Titles: {total_titles}

Total Credits Records: {total_credits}

Total Movies: {total_movies}

Total TV Shows: {total_shows}


AVERAGE RATINGS:

Average IMDb Rating: {average_imdb:.2f}

Average TMDB Rating: {average_tmdb:.2f}


RELEASE YEAR:

Oldest Release Year: {oldest_year}

Latest Release Year: {latest_year}


TOP 10 GENRES:

{top_genres.to_string()}


TOP 10 PRODUCTION COUNTRIES:

{top_countries.to_string()}


YEAR-WISE CONTENT DISTRIBUTION:

{yearly_content.to_string()}


IMPORTANT DATASET LIMITATIONS:

This dataset contains content catalogue information.

It does not contain actual revenue, sales, subscriptions,
viewership, profit or customer engagement metrics.

IMDb and TMDB ratings represent ratings, not actual
Amazon Prime streaming performance.

Use only the information provided above.
"""


# ==========================================
# 10. AI QUESTION ANSWERING SYSTEM
# ==========================================

st.subheader("🤖 Ask Your AI Business Intelligence Assistant")

st.write(
    "Ask questions about movies, TV shows, genres, "
    "ratings, countries and content trends."
)


if "messages" not in st.session_state:

    st.session_state.messages = []


# Display previous conversation

for message in st.session_state.messages:

    with st.chat_message(message["role"]):

        st.markdown(message["content"])


# User input

user_question = st.chat_input(
    "Ask something about Amazon Prime data..."
)


if user_question:

    st.session_state.messages.append(
        {
            "role": "user",
            "content": user_question
        }
    )

    with st.chat_message("user"):

        st.markdown(user_question)


    with st.chat_message("assistant"):

        with st.spinner("Analysing your question..."):

            try:

                conversation_history = ""

                for message in st.session_state.messages[-10:]:

                    conversation_history += (
                        f"\n{message['role']}: {message['content']}"
                    )


                prompt = f"""

You are an experienced Business Intelligence Analyst.

Answer the user's question using ONLY the dataset context
provided below.

DATASET CONTEXT:

{data_context}


CONVERSATION HISTORY:

{conversation_history}


INSTRUCTIONS:

1. Give clear and accurate answers.
2. Use actual dataset metrics.
3. Explain business insights in simple language.
4. Do not invent revenue, sales, profit or subscriber figures.
5. Do not claim ratings represent actual streaming performance.
6. If the required information is unavailable, clearly say so.
7. Use tables or bullet points when useful.
8. Distinguish between data-backed findings and suggestions.


USER QUESTION:

{user_question}

"""


                response = client.models.generate_content(
                    model="gemini-3.8-flash",
                    contents=prompt
                )

                answer = response.text

                if not answer:

                    answer = "Gemini returned an empty response."


                st.markdown(answer)

                st.session_state.messages.append(
                    {
                        "role": "assistant",
                        "content": answer
                    }
                )


            except Exception as e:

                st.error(f"AI Assistant Error: {e}")


# ==========================================
# 11. FOOTER
# ==========================================

st.divider()

st.caption(
    "AI-Powered Amazon Prime Content Intelligence System | "
    "Python | Pandas | Streamlit | Gemini API"
)