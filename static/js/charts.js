function renderCharts() {
  const container = document.getElementById('chartsContainer');
  if (!container || !chartData) return;

  chartData.charts.forEach(chart => {
    const wrapper = document.createElement('div');
    wrapper.className = 'chart-wrapper';
    wrapper.innerHTML = `<p class="chart-title">${chart.title}</p><canvas></canvas>`;
    container.appendChild(wrapper);
    const canvas = wrapper.querySelector('canvas');
    const colors = ['#4f46e5','#06b6d4','#10b981','#f59e0b','#ef4444','#8b5cf6','#ec4899'];

    if (chart.type === 'bar') {
      new Chart(canvas, { type: 'bar', data: { labels: chart.labels, datasets: [{ data: chart.data, backgroundColor: '#4f46e520', borderColor: '#4f46e5', borderWidth: 1.5 }] }, options: { plugins: { legend: { display: false } }, scales: { y: { grid: { color: '#f3f4f6' } }, x: { grid: { display: false } } } } });
    } else if (chart.type === 'scatter') {
      const pts = chart.x.map((x, i) => ({ x, y: chart.y[i] }));
      new Chart(canvas, { type: 'scatter', data: { datasets: [{ data: pts, backgroundColor: '#4f46e580', pointRadius: 4 }] }, options: { plugins: { legend: { display: false } }, scales: { x: { title: { display: true, text: chart.x_label } }, y: { title: { display: true, text: chart.y_label } } } } });
    } else if (chart.type === 'pie') {
      new Chart(canvas, { type: 'doughnut', data: { labels: chart.labels, datasets: [{ data: chart.data, backgroundColor: colors.slice(0, chart.data.length) }] }, options: { plugins: { legend: { position: 'bottom' } } } });
    }
  });
}

function sendMessage() {
  const input = document.getElementById('chatInput');
  const messages = document.getElementById('chatMessages');
  const btn = document.getElementById('sendBtn');
  const text = input.value.trim();
  if (!text) return;

  messages.innerHTML += `<div class="message user"><div class="msg-content">${text}</div></div>`;
  input.value = '';
  btn.disabled = true;
  messages.innerHTML += `<div class="message assistant" id="typing"><div class="msg-content">Thinking...</div></div>`;
  messages.scrollTop = messages.scrollHeight;

  fetch(`/chat/${fileId}`, { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify({ message: text }) })
    .then(r => r.json())
    .then(data => {
      document.getElementById('typing').remove();
      const reply = data.response || data.error || 'Something went wrong.';
      messages.innerHTML += `<div class="message assistant"><div class="msg-content">${reply.replace(/\n/g, '<br>')}</div></div>`;
      messages.scrollTop = messages.scrollHeight;
      btn.disabled = false;
    });
}

document.addEventListener('DOMContentLoaded', () => {
  renderCharts();
  const input = document.getElementById('chatInput');
  if (input) {
    input.addEventListener('keydown', e => { if (e.key === 'Enter' && !e.shiftKey) { e.preventDefault(); sendMessage(); } });
  }
});