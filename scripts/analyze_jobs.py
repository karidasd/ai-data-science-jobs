import urllib.request
import json
import re
import os
from datetime import datetime

SKILLS = {
    "Python": ["python"],
    "SQL": ["sql"],
    "R": [" r ", " r,", " r.", ">r<", ">r ", " r\n"],
    "Java": ["java ", "java,", "java."],
    "C++": ["c++", "c/c++"],
    "PyTorch": ["pytorch"],
    "TensorFlow": ["tensorflow", " tf ", " tf,", " tf."],
    "Keras": ["keras"],
    "Scikit-Learn": ["scikit", "sklearn"],
    "Pandas": ["pandas"],
    "NumPy": ["numpy"],
    "Spark": ["spark", "pyspark"],
    "Hadoop": ["hadoop"],
    "Kafka": ["kafka"],
    "Docker": ["docker"],
    "Kubernetes": ["kubernetes", "k8s"],
    "AWS": ["aws", "amazon web services"],
    "GCP": ["gcp", "google cloud"],
    "Azure": ["azure"],
    "Tableau": ["tableau"],
    "Power BI": ["powerbi", "power bi"],
    "LLM": ["llm", "large language model"],
    "RAG": ["rag", "retrieval augmented generation", "retrieval-augmented generation"],
    "LangChain": ["langchain"],
    "OpenAI": ["openai"],
    "Hugging Face": ["huggingface", "hugging face"],
    "Airflow": ["airflow", "apache airflow"],
    "Snowflake": ["snowflake"],
    "Databricks": ["databricks"],
    "Git": ["git", "github", "gitlab"],
    "Linux": ["linux"]
}

def clean_html(raw_html):
    cleanr = re.compile('<.*?>')
    cleantext = re.sub(cleanr, ' ', raw_html)
    return cleantext.lower()

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

def analyze_skills(jobs):
    total_jobs = len(jobs)
    if total_jobs == 0:
        return []

    skill_counts = {skill: 0 for skill in SKILLS.keys()}
    
    for job in jobs:
        desc = job['description'] + " " + job['title'].lower()
        for skill, keywords in SKILLS.items():
            for kw in keywords:
                if kw in desc:
                    skill_counts[skill] += 1
                    break  # Count once per job

    results = []
    for skill, count in skill_counts.items():
        percentage = round((count / total_jobs) * 100, 1)
        results.append({
            "skill": skill,
            "count": count,
            "percentage": percentage
        })
        
    # Sort descending by count
    results.sort(key=lambda x: x['count'], reverse=True)
    return results

def main():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    data_dir = os.path.join(script_dir, '..', 'data')
    os.makedirs(data_dir, exist_ok=True)
    
    jobs = fetch_jobs()
    print(f"Total jobs collected: {len(jobs)}")
    
    skill_stats = analyze_skills(jobs)
    
    # Save the output
    output_file = os.path.join(data_dir, 'skills.json')
    with open(output_file, 'w', encoding='utf-8') as f:
        json_data = {
            "last_updated": datetime.now().strftime('%Y-%m-%d %H:%M'),
            "total_jobs_analyzed": len(jobs),
            "skills": skill_stats
        }
        json.dump(json_data, f, indent=4, ensure_ascii=False)
        
    print(f"Saved skill analysis to {output_file}")

if __name__ == "__main__":
    main()
