import urllib.request
import json
import re
import os
from datetime import datetime

CATEGORIES = {
    "Programming Languages": {
        "Python": ["python"],
        "SQL": ["sql"],
        "R": [" r ", " r,", " r.", ">r<", ">r ", " r\n"],
        "Java": ["java ", "java,", "java."],
        "C++": ["c++", "c/c++"]
    },
    "AI & Machine Learning": {
        "PyTorch": ["pytorch"],
        "TensorFlow": ["tensorflow", " tf ", " tf,", " tf."],
        "LLM": ["llm", "large language model"],
        "RAG": ["rag", "retrieval augmented generation", "retrieval-augmented generation"],
        "LangChain": ["langchain"],
        "OpenAI API": ["openai", "gpt-4", "gpt-3"],
        "Hugging Face": ["huggingface", "hugging face"],
        "Scikit-Learn": ["scikit", "sklearn"],
        "Pandas": ["pandas"],
        "NumPy": ["numpy"]
    },
    "Cloud & MLOps": {
        "AWS": ["aws", "amazon web services"],
        "Docker": ["docker"],
        "Kubernetes": ["kubernetes", "k8s"],
        "GCP": ["gcp", "google cloud"],
        "Azure": ["azure"],
        "Airflow": ["airflow", "apache airflow"],
        "Spark": ["spark", "pyspark"],
        "Git": ["git", "github", "gitlab"],
        "Snowflake": ["snowflake"],
        "Tableau": ["tableau"],
        "Power BI": ["powerbi", "power bi"]
    }
}

def clean_html(raw_html):
    cleanr = re.compile('<.*?>')
    cleantext = re.sub(cleanr, ' ', raw_html)
    return cleantext.lower()

def extract_salary(text):
    # Regex to find patterns like $120k, $100,000, 150k USD
    match = re.search(r'\$[\d,]{2,}k?|\b\d{2,3}k\s*usd\b', text, re.IGNORECASE)
    if match:
        return match.group(0).upper()
    return None

def fetch_jobs():
    jobs = []
    
    # 1. Remotive (Data)
    try:
        req = urllib.request.Request('https://remotive.com/api/remote-jobs?category=data', headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req) as response:
            data = json.loads(response.read().decode())
            for j in data.get('jobs', []):
                jobs.append({
                    'title': j.get('title', ''),
                    'company': j.get('company_name', ''),
                    'url': j.get('url', ''),
                    'description': clean_html(j.get('description', ''))
                })
        print(f"Fetched {len(data.get('jobs', []))} from Remotive.")
    except Exception as e:
        print(f"Error fetching from Remotive: {e}")

    # 2. Jobicy (Data Science)
    try:
        req = urllib.request.Request('https://jobicy.com/api/v2/remote-jobs?industry=data-science', headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req) as response:
            data = json.loads(response.read().decode())
            for j in data.get('jobs', []):
                jobs.append({
                    'title': j.get('jobTitle', ''),
                    'company': j.get('companyName', ''),
                    'url': j.get('url', ''),
                    'description': clean_html(j.get('jobDescription', ''))
                })
        print(f"Fetched {len(data.get('jobs', []))} from Jobicy.")
    except Exception as e:
        print(f"Error fetching from Jobicy: {e}")

    return jobs

def get_previous_data(filepath):
    if os.path.exists(filepath):
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                old_data = json.load(f)
                old_percentages = {}
                for cat in old_data.get('categories', {}).values():
                    for skill in cat:
                        old_percentages[skill['skill']] = skill['percentage']
                return old_percentages
        except:
            return {}
    return {}

def analyze_jobs(jobs, previous_percentages):
    total_jobs = len(jobs)
    if total_jobs == 0:
        return {}, []

    # Initialize skill counts
    skill_counts = {}
    for cat, skills_dict in CATEGORIES.items():
        skill_counts[cat] = {skill: 0 for skill in skills_dict.keys()}

    valid_jobs_list = []

    for job in jobs:
        desc = job['description'] + " " + job['title'].lower()
        salary = extract_salary(desc)
        found_skills = []

        for cat, skills_dict in CATEGORIES.items():
            for skill, keywords in skills_dict.items():
                for kw in keywords:
                    if kw in desc:
                        skill_counts[cat][skill] += 1
                        found_skills.append(skill)
                        break  # Count once per job per skill

        if found_skills:
            valid_jobs_list.append({
                "title": job['title'],
                "company": job['company'],
                "url": job['url'],
                "salary": salary,
                "skills": found_skills
            })

    # Prepare categories output
    categories_output = {}
    for cat, skills_dict in skill_counts.items():
        cat_list = []
        for skill, count in skills_dict.items():
            percentage = round((count / total_jobs) * 100, 1)
            old_pct = previous_percentages.get(skill, percentage)
            trend = round(percentage - old_pct, 1)
            
            cat_list.append({
                "skill": skill,
                "count": count,
                "percentage": percentage,
                "trend": trend
            })
        # Sort descending by count
        cat_list.sort(key=lambda x: x['count'], reverse=True)
        categories_output[cat] = cat_list

    # Return categories and top 30 valid jobs
    return categories_output, valid_jobs_list[:30]

def main():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    data_dir = os.path.join(script_dir, '..', 'data')
    os.makedirs(data_dir, exist_ok=True)
    
    output_file = os.path.join(data_dir, 'skills.json')
    
    # Get old percentages for trend calculation
    previous_percentages = get_previous_data(output_file)
    
    jobs = fetch_jobs()
    print(f"Total jobs collected: {len(jobs)}")
    
    categories_stats, top_jobs = analyze_jobs(jobs, previous_percentages)
    
    # Save the output
    with open(output_file, 'w', encoding='utf-8') as f:
        json_data = {
            "last_updated": datetime.now().strftime('%Y-%m-%d %H:%M'),
            "total_jobs_analyzed": len(jobs),
            "categories": categories_stats,
            "latest_jobs": top_jobs
        }
        json.dump(json_data, f, indent=4, ensure_ascii=False)
        
    print(f"Saved skill analysis and {len(top_jobs)} live jobs to {output_file}")

if __name__ == "__main__":
    main()
