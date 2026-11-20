import os
import sys
from pathlib import Path

from dotenv import load_dotenv
from google import genai


# ==========================================
# 1. PROJECT PATH AND ENVIRONMENT VARIABLES
# ==========================================

BASE_DIR = Path(__file__).resolve().parent.parent

# Add project root to Python path
sys.path.insert(0, str(BASE_DIR))

# Load shared data processing function
from src.data_processing import load_and_clean_data

# Load API key from project root .env file
load_dotenv(BASE_DIR / ".env")

API_KEY = os.getenv("GEMINI_API_KEY")

if not API_KEY:
    raise ValueError(
        "Gemini API Key not found. Please check your .env file."
    )

client = genai.Client(api_key=API_KEY)


# ==========================================
# 2. LOAD CLEANED DATASETS
# ==========================================

titles, credits = load_and_clean_data()

print("\nCleaned datasets loaded successfully!")
print("Total Titles:", len(titles))
print("Total Credits:", len(credits))


# ==========================================
# 3. BASIC DATA ANALYSIS
# ==========================================

total_titles = len(titles)
total_credits = len(credits)

content_distribution = titles["type"].value_counts()

content_percentage = (
    titles["type"].value_counts(normalize=True) * 100
)

average_imdb_score = titles["imdb_score"].mean()
average_tmdb_score = titles["tmdb_score"].mean()

latest_release_year = titles["release_year"].max()
oldest_release_year = titles["release_year"].min()


# ==========================================
# 4. TOP 10 GENRES
# ==========================================

top_genres = (
    titles["genres"]
    .explode()
    .dropna()
    .value_counts()
    .head(10)
)


# ==========================================
# 5. TOP 10 PRODUCTION COUNTRIES
# ==========================================

top_countries = (
    titles["production_countries"]
    .explode()
    .dropna()
    .value_counts()
    .head(10)
)


# ==========================================
# 6. YEAR-WISE CONTENT ANALYSIS
# ==========================================

yearly_content = (
    titles.groupby("release_year")
    .size()
    .sort_index()
)

recent_years = yearly_content.tail(10)


# ==========================================
# 7. DISPLAY ANALYSIS RESULTS
# ==========================================

print("\n========== AMAZON PRIME DATA ANALYSIS ==========")

print("\nTotal Titles:", total_titles)

print("\nTotal Credits:", total_credits)

print("\nContent Distribution:")
print(content_distribution)

print("\nContent Percentage:")
print(content_percentage.round(2))

print("\nAverage IMDb Score:", round(average_imdb_score, 2))

print("\nAverage TMDB Score:", round(average_tmdb_score, 2))

print("\nOldest Release Year:", oldest_release_year)

print("\nLatest Release Year:", latest_release_year)

print("\nTop 10 Genres:")
print(top_genres)

print("\nTop 10 Production Countries:")
print(top_countries)

print("\nContent Released in Recent 10 Years Available:")
print(recent_years)


# ==========================================
# 8. PREPARE BUSINESS DATA FOR GEMINI
# ==========================================

business_data = f"""
You are an experienced Business Intelligence Analyst.

Analyse the following Amazon Prime content catalogue dataset.

DATASET OVERVIEW:

Total Titles: {total_titles}

Total Credits Records: {total_credits}


CONTENT DISTRIBUTION:

{content_distribution.to_string()}


CONTENT PERCENTAGE:

{content_percentage.round(2).to_string()}


AVERAGE RATINGS:

Average IMDb Score: {average_imdb_score:.2f}

Average TMDB Score: {average_tmdb_score:.2f}


RELEASE YEAR:

Oldest Release Year: {oldest_release_year}

Latest Release Year: {latest_release_year}


TOP 10 GENRES:

{top_genres.to_string()}


TOP 10 PRODUCTION COUNTRIES:

{top_countries.to_string()}


RECENT YEAR-WISE CONTENT DISTRIBUTION:

{recent_years.to_string()}


YOUR TASK:

Generate a professional Business Intelligence Report containing:

1. Executive Summary
2. Key Business Insights
3. Content Catalogue and Ratings Analysis
4. Potential Business Opportunities
5. Five Data-Driven Business Recommendations


IMPORTANT INSTRUCTIONS:

- Use only the metrics and information provided.
- Do not invent revenue, sales, subscribers, viewership or profit figures.
- Do not claim that ratings represent actual streaming performance.
- Explain content catalogue trends using the available data.
- Mention limitations wherever information is insufficient.
- Make recommendations practical and relevant to content portfolio analysis.
- Use professional and easy-to-understand business language.
"""


# ==========================================
# 9. GENERATE AI BUSINESS INSIGHTS
# ==========================================

try:

    print("\nConnecting to Gemini AI...")

    response = client.models.generate_content(
        model="gemini-3.8-flash",
        contents=business_data
    )

    report = response.text

    if not report:
        raise ValueError("Gemini returned an empty response.")

    print("\n========== AI BUSINESS INTELLIGENCE REPORT ==========")

    print(report)


    # ==========================================
    # 10. SAVE AI REPORT
    # ==========================================

    reports_dir = BASE_DIR / "reports"

    reports_dir.mkdir(parents=True, exist_ok=True)

    report_path = reports_dir / "AI_Business_Insights.txt"

    with open(
        report_path,
        "w",
        encoding="utf-8"
    ) as file:

        file.write(report)

    print("\n==========================================")
    print("AI BUSINESS REPORT GENERATED SUCCESSFULLY!")
    print("Report saved in reports folder.")
    print("File: AI_Business_Insights.txt")
    print("==========================================")


except Exception as e:

    print("\nGemini API Error:", e)