// Show loading spinner modal on form submit
const analyzeForm = document.getElementById('analyze-form');
if (analyzeForm) {
  analyzeForm.addEventListener('submit', function() {
    const modal = new bootstrap.Modal(document.getElementById('loadingModal'));
    modal.show();
  });
}

// --- Visual Analytics (Chart.js) ---
function getContext(id) {
  const el = document.getElementById(id);
  return el ? el.getContext('2d') : null;
}

// These variables will be injected by Jinja in results.html
if (window.matchedSkills && window.missingSkills && typeof window.fitScore !== 'undefined') {
  // Pie chart: Skill coverage
  const pieCtx = getContext('skillsPieChart');
  if (pieCtx) {
    new Chart(pieCtx, {
      type: 'pie',
      data: {
        labels: ['Matched', 'Missing'],
        datasets: [{
          data: [window.matchedSkills.length, window.missingSkills.length],
          backgroundColor: ['#2563eb', '#e11d48'],
        }]
      },
      options: {
        plugins: {
          legend: { display: true, position: 'bottom' },
          datalabels: { display: false }
        }
      }
    });
  }
  // Gauge: Match score
  const gaugeCtx = getContext('matchScoreGauge');
  if (gaugeCtx) {
    new Chart(gaugeCtx, {
      type: 'doughnut',
      data: {
        labels: ['Fit Score', ''],
        datasets: [{
          data: [window.fitScore, 100 - window.fitScore],
          backgroundColor: ['#22c55e', '#e5e7eb'],
          borderWidth: 0
        }]
      },
      options: {
        rotation: -90,
        circumference: 180,
        cutout: '80%',
        plugins: {
          legend: { display: false },
          datalabels: { display: false },
          tooltip: { enabled: false },
        },
      },
      plugins: [{
        id: 'scoreText',
        afterDraw(chart) {
          const { ctx, chartArea } = chart;
          ctx.save();
          ctx.font = 'bold 2rem sans-serif';
          ctx.fillStyle = '#22c55e';
          ctx.textAlign = 'center';
          ctx.textBaseline = 'middle';
          ctx.fillText(window.fitScore + '%', chart.width / 2, chart.height * 0.7);
          ctx.restore();
        }
      }]
    });
  }
  // Word cloud (simple): show skills as varying font sizes
  const wordCloud = document.getElementById('skillsWordCloud');
  if (wordCloud) {
    const ctx = wordCloud.getContext('2d');
    ctx.clearRect(0, 0, wordCloud.width, wordCloud.height);
    const allSkills = window.matchedSkills.concat(window.missingSkills);
    let x = 20, y = 60;
    allSkills.forEach((skill, i) => {
      ctx.font = `${16 + (window.matchedSkills.includes(skill) ? 10 : 0)}px sans-serif`;
      ctx.fillStyle = window.matchedSkills.includes(skill) ? '#2563eb' : '#e11d48';
      ctx.fillText(skill, x, y);
      x += ctx.measureText(skill).width + 24;
      if (x > wordCloud.width - 120) { x = 20; y += 32; }
    });
  }
} 