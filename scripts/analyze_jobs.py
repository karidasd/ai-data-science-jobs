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
    seen_urls = set()

    def add_job(title, company, url, desc):
        if url and url not in seen_urls:
            seen_urls.add(url)
            jobs.append({
                'title': title,
                'company': company,
                'url': url,
                'description': clean_html(desc)
            })

    # 1. Remotive (Data & Software Dev)
    for cat in ['data', 'software-dev']:
        try:
            req = urllib.request.Request(f'https://remotive.com/api/remote-jobs?category={cat}', headers={'User-Agent': 'Mozilla/5.0'})
            with urllib.request.urlopen(req) as response:
                data = json.loads(response.read().decode())
                count = 0
                for j in data.get('jobs', []):
                    add_job(j.get('title', ''), j.get('company_name', ''), j.get('url', ''), j.get('description', ''))
                    count += 1
            print(f"Fetched {count} from Remotive ({cat}).")
        except Exception as e:
            print(f"Error fetching from Remotive {cat}: {e}")

    # 2. Jobicy (Data Science & Engineering)
    for ind in ['data-science', 'engineering']:
        try:
            req = urllib.request.Request(f'https://jobicy.com/api/v2/remote-jobs?industry={ind}', headers={'User-Agent': 'Mozilla/5.0'})
            with urllib.request.urlopen(req) as response:
                data = json.loads(response.read().decode())
                count = 0
                for j in data.get('jobs', []):
                    add_job(j.get('jobTitle', ''), j.get('companyName', ''), j.get('url', ''), j.get('jobDescription', ''))
                    count += 1
            print(f"Fetched {count} from Jobicy ({ind}).")
        except Exception as e:
            print(f"Error fetching from Jobicy {ind}: {e}")
            
    # 3. Arbeitnow
    try:
        req = urllib.request.Request('https://www.arbeitnow.com/api/job-board-api', headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req) as response:
            data = json.loads(response.read().decode())
            count = 0
            for j in data.get('data', []):
                add_job(j.get('title', ''), j.get('company_name', ''), j.get('url', ''), j.get('description', ''))
                count += 1
        print(f"Fetched {count} from Arbeitnow.")
    except Exception as e:
        print(f"Error fetching from Arbeitnow: {e}")

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

    unicorn_job = None
    max_score = -1

    for job in valid_jobs_list:
        score = len(job['skills']) * 10
        if job['salary']:
            score += 20
            # give bonus for high salaries
            if any(high_val in job['salary'] for high_val in ['10', '12', '15', '20', '30']):
                score += 30
        
        job['is_unicorn'] = False
        job['_score'] = score
        
        if score > max_score:
            max_score = score
            unicorn_job = job

    if unicorn_job:
        unicorn_job['is_unicorn'] = True
        
    # Sort valid_jobs_list by score descending
    valid_jobs_list.sort(key=lambda x: x['_score'], reverse=True)

    # Return categories and top 100 valid jobs
    return categories_output, valid_jobs_list[:100]

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
