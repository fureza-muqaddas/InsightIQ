# InsightIQ 🔍

An AI-powered data analysis web application that lets you upload datasets and instantly get insights, visualizations, and professional reports through natural language chat.

## 🌐 Live Demo
**[https://insightiq-1-69fa.onrender.com](https://insightiq-1-69fa.onrender.com)**

> Note: App may take 30-60 seconds to load on first visit as it runs on a free server tier.

## ✨ Features

- **Upload & Analyze** — supports CSV, Excel (.xlsx), and JSON files
- **AI Chat** — ask questions about your data in plain English
- **Auto Visualizations** — bar charts, scatter plots, and pie charts generated automatically
- **AI Reports** — generate comprehensive professional reports with one click
- **Data History** — all uploaded datasets and chat history saved locally

## 🛠️ Tech Stack

| Layer | Technology |
|-------|-----------|
| Backend | Python, Flask |
| AI Model | Llama 3.3 70B via Groq API |
| Data Processing | Pandas |
| Database | SQLite + SQLAlchemy |
| Frontend | HTML, CSS, JavaScript, Chart.js |
| Deployment | Render |

## 📁 Project Structure

```
InsightIQ/
├── app.py                 # Flask app & routes
├── config.py              # Configuration & environment variables
├── requirements.txt       # Python dependencies
├── agent/
│   └── analyst.py         # AI analysis logic
├── database/
│   └── models.py          # SQLite database models
├── templates/
│   ├── base.html
│   ├── index.html         # Dashboard
│   ├── chat.html          # AI chat & charts
│   └── report.html        # Generated reports
└── static/
    ├── css/style.css
    └── js/
        ├── upload.js
        └── charts.js
```

## 🚀 Getting Started

### Prerequisites
- Python 3.11+
- Groq API key (free at [console.groq.com](https://console.groq.com))

### Installation

1. Clone the repository
```bash
git clone https://github.com/fureza-muqaddas/insightiq.git
cd insightiq
```

2. Create a virtual environment
```bash
python -m venv venv
venv\Scripts\activate
```

3. Install dependencies
```bash
pip install -r requirements.txt
```

4. Create a `.env` file in the project root
```
GROQ_API_KEY=your_groq_api_key_here
SECRET_KEY=your_secret_key_here
```

5. Run the app
```bash
python app.py
```

6. Open your browser at `http://127.0.0.1:5000`

## 💡 Usage

1. Upload a CSV, Excel, or JSON file on the dashboard
2. Click **Analyze** to view auto-generated charts
3. Ask questions in the chat — e.g. *"Which product has the highest profit margin?"*
4. Click **Generate Report** for a full AI-written analysis

## 🤖 Example Questions to Ask

- "What are the top 5 values in this dataset?"
- "Which category has the highest revenue?"
- "What trends do you see over time?"
- "Give me an executive summary of this data"
- "What anomalies or outliers do you notice?"

## 👤 Author

**Fureza Muqaddas**  
AI & Data Science Professional — Edmonton, Alberta  
[GitHub](https://github.com/fureza-muqaddas) · [LinkedIn](https://linkedin.com/in/fureza_muqaddas/)

## 📄 License
MIT