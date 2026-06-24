# 🎯 AI & Data Science Job Radar

![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![JavaScript](https://img.shields.io/badge/JavaScript-F7DF1E?style=for-the-badge&logo=javascript&logoColor=black)
![GitHub Actions](https://img.shields.io/badge/Automated-GitHub%20Actions-2088FF?style=for-the-badge&logo=github-actions&logoColor=white)
![Data Analysis](https://img.shields.io/badge/NLP-Keyword_Extraction-fbbf24?style=for-the-badge)

An automated, intelligent career strategy tool built for Data Scientists, Machine Learning Engineers, and AI Practitioners. 

🔗 **[View the Live Dashboard Here](https://karidasd.github.io/ai-data-science-jobs/)**

---

## 🚀 Project Overview

The **AI Job Radar** is a serverless application that daily aggregates, analyzes, and ranks remote job opportunities worldwide. Instead of manually scrolling through job boards, this tool uses Python and Natural Language Processing (NLP) to read hundreds of job descriptions, extract demanded tech stacks, find hidden salaries, and present you with the absolute top 100 opportunities of the day.

## ✨ Core Features

- **👑 The Unicorn Job**: A custom scoring algorithm evaluates every scraped job based on the complexity of the AI tech stack and the offered salary. The highest-scoring opportunity is highlighted with a gold border at the top of the board.
- **📈 Tech Stack Market Share**: Skills are dynamically categorized into `Programming Languages`, `AI & Machine Learning`, and `Cloud & MLOps`. The tool displays live percentages of what the market is actually demanding right now.
- **🔄 Market Momentum**: Compares today's skill demands with yesterday's data to show live trend badges (e.g., `📈 +2%` or `📉 -1%`), allowing you to predict which frameworks are becoming mainstream.
- **💰 Salary AI Extractor**: Uses Regular Expressions (Regex) to scan unstructured HTML job descriptions and automatically extract hidden salary bands (e.g., `$120k` or `150,000 USD`).
- **🎯 Smart Filtering & Top 100**: Scrapes ~300 jobs daily from platforms like Remotive, Arbeitnow, and Jobicy. It discards irrelevant roles (Data Entry, Customer Support) and outputs only the Top 100 high-quality Remote jobs.

---

## ⚙️ Technical Architecture

The architecture relies entirely on **Static Site Generation** and **Free CI/CD** (Zero hosting costs).

1. **Data Pipeline (Python)**: `analyze_jobs.py` runs daily, fetches JSON data from multiple free APIs, deduplicates URLs, cleans HTML tags, and extracts keyword matrices.
2. **Automation (GitHub Actions)**: A CRON job (`update.yml`) executes the Python script every midnight, calculates market deltas, and commits the newly generated `skills.json` directly to the repository.
3. **Frontend (Vanilla HTML/JS/CSS)**: A sleek, dark-mode, neon-accented UI reads the static JSON file asynchronously. It features dynamic progress bars and grid layouts, functioning essentially as a serverless Single Page Application (SPA).

---

## 🛠️ How to Run Locally

If you want to test the data extraction pipeline locally:

1. Clone the repository:
   ```bash
   git clone https://github.com/karidasd/ai-data-science-jobs.git
   cd ai-data-science-jobs
   ```
2. Run the Data Pipeline (Python 3.x required, no external libraries needed):
   ```bash
   python scripts/analyze_jobs.py
   ```
3. Open `index.html` in your browser. The dashboard will automatically load the freshly generated `data/skills.json`.

---

## ⚠️ Legal Disclaimer

**EN:** This project is a personal portfolio piece created solely for educational and programming demonstration purposes. It does not provide professional career counseling.
**EL:** ΠΡΟΣΟΧΗ: Το παρόν έργο αποτελεί προσωπικό project (portfolio) καθαρά για εκπαιδευτικούς σκοπούς προγραμματισμού και ανάλυσης δεδομένων. Δεν αποτελεί επαγγελματική συμβουλευτική καριέρας. Δημιουργήθηκε από Δημόσιο Υπάλληλο στον ελεύθερο χρόνο του, εκτός ωραρίου υπηρεσίας, χωρίς καμία απολύτως εμπορική, κερδοσκοπική ή επαγγελματική εκμετάλλευση. Δεν υφίσταται καμία απολύτως οικονομική συναλλαγή.
