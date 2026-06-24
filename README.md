# 🎯 AI & Data Science Job Radar (V3.0)

![Automated](https://img.shields.io/badge/Automated-GitHub%20Actions-10b981?style=for-the-badge)
![NLP](https://img.shields.io/badge/Tech-Python%20NLP-fbbf24?style=for-the-badge)

Ένα στρατηγικό εργαλείο καριέρας για Data Scientists και AI Engineers. Το σύστημα σαρώνει καθημερινά εκατοντάδες Remote αγγελίες εργασίας, εξάγει στατιστικά, αναλύει μισθούς και προβλέπει τάσεις!

🔗 **[Δείτε το Live Dashboard](https://karidasd.github.io/ai-data-science-jobs/)**

## Τι νέο φέρνει η V3.0 (The Ultimate Career Tool)
- **AI Resume Matcher**: Επικολλήστε το βιογραφικό σας (CV) στο νέο πλαίσιο! Η JavaScript θα το σαρώσει τοπικά και θα σας δώσει ένα **Market Readiness Score**, συγκρίνοντάς το με τα Top 10 πιο περιζήτητα skills της ημέρας. Σας λέει ακριβώς τι σας λείπει!
- **The Unicorn Job 👑**: Ο αλγόριθμος Python αξιολογεί τις αγγελίες (βάσει απαιτούμενων AI skills και ύψους μισθού) και επιλέγει την **Κορυφαία Αγγελία της Ημέρας**. Θα τη δείτε να λάμπει με χρυσό περίγραμμα στο Live Job Board!
- **Tech Stack View**: Διαχωρισμός των δεξιοτήτων σε 3 κάρτες (Programming Languages, AI & ML, Cloud & MLOps).
- **Market Momentum**: Υπολογισμός τάσεων (Trend Badges) - βλέπετε τι ανεβαίνει 📈 και τι πέφτει 📉 καθημερινά!
- **Live Job Board**: Το dashboard δεν δείχνει μόνο ποσοστά, αλλά και τις **Top 100 σημερινές Remote αγγελίες εργασίας** με απευθείας links (Apply Now).
- **Salary AI Extractor**: Αυτόματη εύρεση (μέσω Regex) και εξαγωγή του προσφερόμενου μισθού (π.χ. `$120k`) μέσα από το αχανές κείμενο της αγγελίας!

## Πώς Λειτουργεί
1. **Data Collection**: Αντλεί ζωντανά δεδομένα από τα ελεύθερα APIs των `Remotive` και `Jobicy`.
2. **Analysis**: Το Python backend (`scripts/analyze_jobs.py`) διαβάζει τα HTML descriptions, εξάγει τα keywords, αποθηκεύει τους μισθούς και υπολογίζει τις αυξομειώσεις % από την προηγούμενη μέρα.
3. **UI Dashboard**: Η HTML/Vanilla JS σελίδα χτίζει το εντυπωσιακό UI δυναμικά διαβάζοντας το JSON αρχείο.
4. **100% Αυτοματοποίηση**: Όλη η διαδικασία "τρέχει" αυτόματα στους servers της Microsoft (GitHub Actions) 1 φορά την ημέρα. Δεν απαιτείται hosting!
