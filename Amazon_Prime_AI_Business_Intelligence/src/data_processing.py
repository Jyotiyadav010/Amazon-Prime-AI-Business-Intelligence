import pandas as pd
import ast
from pathlib import Path


# Project root directory
BASE_DIR = Path(__file__).resolve().parent.parent

# Dataset paths
TITLES_PATH = BASE_DIR / "data" / "titles.xlsx"
CREDITS_PATH = BASE_DIR / "data" / "credits.xlsx"


def parse_list(value):
    """Convert string representations of lists into Python lists."""

    if isinstance(value, list):
        return value

    if pd.isna(value):
        return []

    try:
        result = ast.literal_eval(value)

        if isinstance(result, list):
            return result

        return [result]

    except (ValueError, SyntaxError, TypeError):
        return [value]


def load_and_clean_data():

    # Load original datasets
    titles = pd.read_excel(TITLES_PATH)
    credits = pd.read_excel(CREDITS_PATH)

    # Create copies to protect original datasets
    titles_clean = titles.copy()
    credits_clean = credits.copy()

    # Remove duplicate records
    titles_clean = titles_clean.drop_duplicates()
    credits_clean = credits_clean.drop_duplicates()

    # Remove rows with missing titles
    titles_clean = titles_clean.dropna(subset=["title"])

    # Fill missing IMDb scores with mean
    titles_clean["imdb_score"] = (
        titles_clean["imdb_score"].fillna(
            titles_clean["imdb_score"].mean()
        )
    )

    # Fill missing runtime with mean
    titles_clean["runtime"] = (
        titles_clean["runtime"].fillna(
            titles_clean["runtime"].mean()
        )
    )

    # Handle missing categorical values
    titles_clean["age_certification"] = (
        titles_clean["age_certification"].fillna("unknown")
    )

    titles_clean["genres"] = (
        titles_clean["genres"].fillna("unknown")
    )

    # Remove unnecessary description column
    titles_clean = titles_clean.drop(columns=["description"])

    # Reset indexes
    titles_clean = titles_clean.reset_index(drop=True)
    credits_clean = credits_clean.reset_index(drop=True)

    # Convert genre and country strings into lists
    titles_clean["genres"] = titles_clean["genres"].apply(parse_list)

    titles_clean["production_countries"] = (
        titles_clean["production_countries"].apply(parse_list)
    )

    return titles_clean, credits_clean


if __name__ == "__main__":

    titles_clean, credits_clean = load_and_clean_data()

    print("\nDATA CLEANING COMPLETED!")
    print("--------------------------------")

    print("Original Titles:", len(pd.read_excel(TITLES_PATH)))
    print("Cleaned Titles:", len(titles_clean))

    print("Original Credits:", len(pd.read_excel(CREDITS_PATH)))
    print("Cleaned Credits:", len(credits_clean))

    print("\nRemaining Missing Values in Titles:")
    print(titles_clean.isnull().sum())

    print("\nRemaining Missing Values in Credits:")
    print(credits_clean.isnull().sum())