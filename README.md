# 🔍 List Comparator

![Python](https://img.shields.io/badge/Python-3.9%2B-blue)
![Streamlit](https://img.shields.io/badge/Streamlit-App-FF4B4B?logo=streamlit&logoColor=white)
![License](https://img.shields.io/badge/License-MIT-green)

A lightweight Streamlit web app for comparing two lists using set
operations and a Venn diagram.

Perfect for gene list overlap, ID comparison, dataset reconciliation,
and general set analysis.

------------------------------------------------------------------------

## 🚀 Features

-   Compare two lists side-by-side
-   Multiple delimiter support (newline, comma, semicolon, whitespace,
    custom)
-   Case-sensitive or case-insensitive comparison
-   Optional whitespace trimming
-   Deduplication toggle
-   Interactive Venn diagram
-   Region exploration (A only / B only / Intersection)
-   Jaccard similarity score
-   Download results as TXT or CSV
-   Efficient set operations (handles large lists)

------------------------------------------------------------------------

## 📦 Installation

### 1️⃣ Clone the repository

git clone https://github.com/your-username/list-comparator.git\
cd list-comparator

### 2️⃣ Create virtual environment (recommended)

python -m venv venv

Activate:

Mac / Linux: source venv/bin/activate

Windows: venv`\Scripts`{=tex}`\activate`{=tex}

### 3️⃣ Install dependencies

pip install -r requirements.txt

------------------------------------------------------------------------

## ▶️ Run the App

streamlit run list_comparator.py

Open in browser:

http://localhost:8501

------------------------------------------------------------------------

## 📁 Project Structure

. ├── list_comparator.py ├── requirements.txt └── README.md

------------------------------------------------------------------------

## 📈 Similarity Metric

Jaccard similarity:

\|A ∩ B\| / \|A ∪ B\|

------------------------------------------------------------------------

## 📝 License

MIT License

------------------------------------------------------------------------

## 👤 Author

Your Name\
GitHub: https://github.com/your-username
