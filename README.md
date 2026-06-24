# 🎯 AI & Data Science Job Radar

![Automated](https://img.shields.io/badge/Automated-GitHub%20Actions-10b981?style=for-the-badge)
![NLP](https://img.shields.io/badge/Tech-Python%20NLP-fbbf24?style=for-the-badge)

Ένα ραντάρ καριέρας για Data Scientists και AI Engineers. Το σύστημα σαρώνει καθημερινά εκατοντάδες Remote αγγελίες εργασίας από παγκόσμιες πλατφόρμες (για Data Science / AI) και εξάγει τα πιο περιζήτητα skills μέσω NLP Keyword Extraction.

🔗 **[Δείτε το Live Dashboard](https://karidasd.github.io/ai-data-science-jobs/)** *(Ενεργοποιήστε τα GitHub Pages!)*

## Πώς Λειτουργεί
1. **Data Collection**: Αντλεί ζωντανά δεδομένα από τα ελεύθερα APIs των `Remotive` και `Jobicy`.
2. **Data Science Analysis**: Καθαρίζει τα HTML descriptions των αγγελιών και μετράει τη συχνότητα εμφάνισης συγκεκριμένων λέξεων-κλειδιών (Python, PyTorch, RAG, LangChain, Kubernetes, κ.ά.).
3. **UI Dashboard**: Απεικονίζει τα αποτελέσματα σε ένα εντυπωσιακό, φουτουριστικό UI με CSS progress bars που δείχνουν το ακριβές % ζήτησης κάθε τεχνολογίας, βάσει των ανοιχτών θέσεων εργασίας!
4. **100% Αυτοματοποίηση**: Τρέχει εντελώς δωρεάν 1 φορά την ημέρα μέσω GitHub Actions.

## Τοπική Εκτέλεση (Local Setup)

1. Κάντε Clone:
```bash
git clone https://github.com/karidasd/ai-data-science-jobs.git
cd ai-data-science-jobs
```

2. Τρέξτε το Python Script (δεν απαιτούνται εξωτερικές βιβλιοθήκες, μόνο τα built-in του Python 3!):
```bash
python scripts/analyze_jobs.py
```

3. Ανοίξτε το αρχείο `index.html` σε οποιονδήποτε browser!
