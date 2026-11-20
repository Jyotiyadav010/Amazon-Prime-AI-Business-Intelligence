# 🎬 Amazon Prime AI-Powered Business Intelligence & Automation System

## 📌 Project Overview

This project focuses on analyzing Amazon Prime Video content data using Python, Power BI, Streamlit, and Google Gemini API.

It combines data analysis, interactive dashboards, AI-powered insights, and automated report generation to make content-related data easier to understand.

## 🛠️ Technologies Used

- Python
- Pandas
- Jupyter Notebook
- Power BI
- Streamlit
- Google Gemini API
- ReportLab

## 📂 Project Structure

```text
Amazon_Prime_AI_Business_Intelligence/
│
├── data/
│   ├── titles.xlsx
│   └── credits.xlsx
│
├── notebooks/
│   └── Amazon_Prime_EDA.ipynb
│
├── dashboard/
│   └── Amazon_Prime_Dashboard.pbix
│
├── src/
│   ├── data_processing.py
│   ├── ai_insights.py
│   └── report_automation.py
│
├── reports/
│   ├── AI_Business_Insights.txt
│   └── AI_Business_Intelligence_Report.pdf
│
├── screenshots/
│
├── app.py
├── run_pipeline.py
├── requirements.txt
└── .gitignore
```

## 📊 Project Features

### 1. Exploratory Data Analysis (EDA)
- Analyzed Amazon Prime Video titles and credits data.
- Explored Movies and TV Shows distribution.
- Analyzed genres and production countries.
- Studied release-year trends.
- Examined IMDb and TMDB ratings.

### 2. Data Cleaning & Processing
- Removed duplicate records.
- Handled missing values.
- Processed genre and production-country columns.
- Created a reusable data processing module.

### 3. Power BI Dashboard
- Total Titles, Movies and TV Shows.
- Average IMDb and TMDB Ratings.
- Top Genres.
- Top Actors and Directors.
- Country-wise content distribution.
- Content release trends.
- Interactive filters.

### 4. AI-Powered Insights
- Integrated Google Gemini API.
- Generated AI-based insights from dataset summaries.
- Enabled users to ask questions about the available dataset.

### 5. Automated Reporting
- Generated AI insights in a text file.
- Converted insights into a PDF business report using Python.

### 6. Streamlit Application
- Interactive dashboard.
- Key business metrics.
- Data visualizations.
- AI-powered Question & Answer functionality.

## ▶️ How to Run the Project

**Step 1: Clone the repository**

```bash
git clone https://github.com/your-username/Amazon-Prime-AI-Business-Intelligence.git
```

**Step 2: Install dependencies**

```bash
pip install -r requirements.txt
```

**Step 3: Configure API Key**

Create a `.env` file in the project folder:

```text
GEMINI_API_KEY=your_api_key
```

**Step 4: Run the Streamlit application**

```bash
python -m streamlit run app.py
```

## ⚠️ Dataset Limitation

The dataset contains content information, credits, genres, release years, and IMDb/TMDB ratings.

It does not contain actual views, watch time, subscribers, revenue, or profit data. Therefore, the analysis focuses on content catalogue insights rather than actual streaming business performance.

## 👩‍💻 Project Purpose

This project demonstrates practical skills in Python, Data Analysis, Data Visualization, Power BI, AI Integration, and Reporting Automation.
