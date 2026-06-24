document.addEventListener('DOMContentLoaded', () => {
    fetchData();
});

async function fetchData() {
    try {
        const timestamp = new Date().getTime();
        const response = await fetch(`data/skills.json?t=${timestamp}`);
        if (!response.ok) throw new Error('Failed to fetch data');
        
        const data = await response.json();
        
        // Update stats
        const statsHtml = `
            <div class="stat-badge">🕒 Updated: ${data.last_updated}</div>
            <div class="stat-badge" style="color: var(--neon-purple);">💼 Jobs Analyzed: ${data.total_jobs_analyzed}</div>
        `;
        document.getElementById('stats-container').innerHTML = statsHtml;
        
        // Render skills
        const listContainer = document.getElementById('skills-list');
        listContainer.innerHTML = '';
        
        data.skills.forEach((skill, index) => {
            // Only show skills that appeared at least once
            if (skill.count === 0) return;
            
            const html = `
                <div class="skill-item" style="animation-delay: ${index * 0.05}s">
                    <div class="skill-info">
                        <span class="skill-name">${skill.skill} <span style="font-size:0.8rem; color:var(--text-secondary)">(${skill.count} jobs)</span></span>
                        <span class="skill-percent">${skill.percentage}%</span>
                    </div>
                    <div class="progress-track">
                        <div class="progress-fill" style="width: 0%" data-target="${skill.percentage}%"></div>
                    </div>
                </div>
            `;
            listContainer.insertAdjacentHTML('beforeend', html);
        });
        
        // Trigger animations after a tiny delay for DOM to register initial 0% width
        setTimeout(() => {
            document.querySelectorAll('.progress-fill').forEach(bar => {
                bar.style.width = bar.getAttribute('data-target');
            });
        }, 100);
        
    } catch (error) {
        console.error('Error:', error);
        document.getElementById('skills-list').innerHTML = '<p style="color:red; text-align:center;">Failed to load data. Please ensure the python script has run.</p>';
    }
}
