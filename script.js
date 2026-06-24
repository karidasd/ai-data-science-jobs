document.addEventListener('DOMContentLoaded', () => {
    fetchData();
});

async function fetchData() {
    try {
        const timestamp = new Date().getTime();
        const response = await fetch(`data/skills.json?t=${timestamp}`);
        if (!response.ok) throw new Error('Failed to fetch data');
        
        const data = await response.json();
        
        // Render Stats
        const statsHtml = `
            <div class="stat-badge" style="color: var(--text-secondary);">🕒 Updated: ${data.last_updated}</div>
            <div class="stat-badge" style="color: var(--neon-green);">💼 Live Remote Jobs: ${data.total_jobs_analyzed}</div>
            <div class="stat-badge" style="color: var(--neon-purple);">🧠 AI Powered NLP</div>
        `;
        document.getElementById('stats-container').innerHTML = statsHtml;
        
        // Render Categories
        const categoriesContainer = document.getElementById('categories-grid');
        categoriesContainer.innerHTML = '';
        
        Object.entries(data.categories).forEach(([catName, skills]) => {
            let skillsHtml = '';
            
            skills.forEach(skill => {
                if (skill.count === 0) return;
                
                // Trend Badge Logic
                let trendHtml = '';
                if (skill.trend > 0) {
                    trendHtml = `<span class="trend-badge trend-up">📈 +${skill.trend}%</span>`;
                } else if (skill.trend < 0) {
                    trendHtml = `<span class="trend-badge trend-down">📉 ${skill.trend}%</span>`;
                } else {
                    trendHtml = `<span class="trend-badge trend-neutral">-</span>`;
                }
                
                skillsHtml += `
                    <div class="skill-item">
                        <div class="skill-info">
                            <span class="skill-name">${skill.skill}</span>
                            <div class="skill-meta">
                                ${trendHtml}
                                <span class="skill-percent">${skill.percentage}%</span>
                            </div>
                        </div>
                        <div class="progress-track">
                            <div class="progress-fill" style="width: 0%" data-target="${skill.percentage}%"></div>
                        </div>
                    </div>
                `;
            });
            
            // Only create card if it has skills
            if (skillsHtml !== '') {
                const cardHtml = `
                    <div class="category-card">
                        <h3 class="category-title">${catName}</h3>
                        <div class="skills-list">
                            ${skillsHtml}
                        </div>
                    </div>
                `;
                categoriesContainer.insertAdjacentHTML('beforeend', cardHtml);
            }
        });
        
        // Render Live Jobs
        const jobsContainer = document.getElementById('job-list');
        jobsContainer.innerHTML = '';
        
        if (data.latest_jobs && data.latest_jobs.length > 0) {
            data.latest_jobs.forEach(job => {
                const tagsHtml = job.skills.map(skill => `<span class="tag">${skill}</span>`).join('');
                const salaryBadge = job.salary ? `<span class="salary-badge">💰 Est: ${job.salary}</span>` : '';
                
                const jobHtml = `
                    <div class="job-card">
                        <div class="job-details">
                            <h3 class="job-title">${job.title}</h3>
                            <div class="job-company">
                                🏢 ${job.company}
                                ${salaryBadge}
                            </div>
                            <div class="job-tags">
                                ${tagsHtml}
                            </div>
                        </div>
                        <a href="${job.url}" target="_blank" rel="noopener noreferrer" class="apply-btn">Apply Now</a>
                    </div>
                `;
                jobsContainer.insertAdjacentHTML('beforeend', jobHtml);
            });
        } else {
            jobsContainer.innerHTML = '<p style="color:var(--text-secondary)">No recent jobs found matching the AI Stack.</p>';
        }
        
        // Trigger Progress Bar Animations
        setTimeout(() => {
            document.querySelectorAll('.progress-fill').forEach(bar => {
                bar.style.width = bar.getAttribute('data-target');
            });
        }, 100);
        
    } catch (error) {
        console.error('Error:', error);
        document.getElementById('categories-grid').innerHTML = '<p style="color:red;">Failed to load data. Please ensure the backend script has run.</p>';
    }
}
