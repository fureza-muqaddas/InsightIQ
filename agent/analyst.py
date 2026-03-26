import pandas as pd
import json
import requests
from config import Config

GROQ_API_URL = "https://api.groq.com/openai/v1/chat/completions"
GROQ_MODEL = "llama-3.3-70b-versatile"

def groq_chat(system_prompt: str, messages: list) -> str:
    headers = {
        "Authorization": f"Bearer {Config.GROQ_API_KEY}",
        "Content-Type": "application/json",
    }
    payload = {
        "model": GROQ_MODEL,
        "max_tokens": 2048,
        "messages": [{"role": "system", "content": system_prompt}] + messages,
    }
    response = requests.post(GROQ_API_URL, headers=headers, json=payload)
    print("GROQ STATUS:", response.status_code)
    print("GROQ RESPONSE:", response.text)
    response.raise_for_status()
    return response.json()["choices"][0]["message"]["content"]

def load_dataframe(filepath: str) -> pd.DataFrame:
    if filepath.endswith(".csv"):
        return pd.read_csv(filepath)
    elif filepath.endswith((".xlsx", ".xls")):
        return pd.read_excel(filepath)
    elif filepath.endswith(".json"):
        return pd.read_json(filepath)
    raise ValueError("Unsupported file type")

def get_data_summary(df: pd.DataFrame) -> str:
    summary = {
        "rows": len(df),
        "columns": list(df.columns),
        "dtypes": {col: str(dtype) for col, dtype in df.dtypes.items()},
        "missing_values": df.isnull().sum().to_dict(),
        "numeric_stats": df.describe().to_dict() if not df.select_dtypes(include="number").empty else {},
        "sample": df.head(5).to_dict(orient="records"),
    }
    return json.dumps(summary, default=str)

def chat_with_data(filepath: str, messages: list, user_message: str) -> str:
    df = load_dataframe(filepath)
    data_summary = get_data_summary(df)

    system_prompt = f"""You are an expert data analyst AI. You help users understand and analyze their data.

Current dataset summary:
{data_summary}

Full data (first 50 rows):
{df.head(50).to_csv(index=False)}

Instructions:
- Answer questions about the data clearly and concisely
- When asked for calculations, show the result
- Suggest insights and patterns you notice
- Always be specific with numbers from the actual data"""

    api_messages = messages + [{"role": "user", "content": user_message}]
    return groq_chat(system_prompt, api_messages)

def generate_report(filepath: str) -> dict:
    df = load_dataframe(filepath)
    data_summary = get_data_summary(df)

    prompt = f"""Analyze this dataset and generate a comprehensive professional report.

Dataset summary:
{data_summary}

Full data:
{df.head(100).to_csv(index=False)}

Generate a report with these sections:
1. Executive Summary
2. Data Overview
3. Key Findings (at least 5 specific insights with numbers)
4. Statistical Analysis
5. Trends & Patterns
6. Recommendations
7. Conclusion

Be specific with numbers and percentages from the data."""

    report_text = groq_chat("You are a professional data analyst.", [{"role": "user", "content": prompt}])

    sections = {}
    current_section = "overview"
    current_content = []

    for line in report_text.split("\n"):
        if line.startswith("#") or (line and line[0].isdigit() and "." in line[:3]):
            if current_content:
                sections[current_section] = "\n".join(current_content).strip()
            current_section = line.strip("# ").strip()
            current_content = []
        else:
            current_content.append(line)

    if current_content:
        sections[current_section] = "\n".join(current_content).strip()

    return {"full_report": report_text, "sections": sections}

def generate_chart_data(filepath: str, chart_type: str = "auto") -> dict:
    df = load_dataframe(filepath)
    numeric_cols = df.select_dtypes(include="number").columns.tolist()
    categorical_cols = df.select_dtypes(include=["object", "category"]).columns.tolist()

    charts = []

    if numeric_cols:
        charts.append({
            "type": "bar",
            "title": f"Distribution of {numeric_cols[0]}",
            "labels": list(range(min(20, len(df)))),
            "data": df[numeric_cols[0]].head(20).tolist(),
            "column": numeric_cols[0],
        })

    if len(numeric_cols) >= 2:
        charts.append({
            "type": "scatter",
            "title": f"{numeric_cols[0]} vs {numeric_cols[1]}",
            "x": df[numeric_cols[0]].head(100).tolist(),
            "y": df[numeric_cols[1]].head(100).tolist(),
            "x_label": numeric_cols[0],
            "y_label": numeric_cols[1],
        })

    if categorical_cols and numeric_cols:
        grouped = df.groupby(categorical_cols[0])[numeric_cols[0]].mean().head(10)
        charts.append({
            "type": "pie",
            "title": f"{numeric_cols[0]} by {categorical_cols[0]}",
            "labels": grouped.index.tolist(),
            "data": grouped.values.tolist(),
        })

    return {"charts": charts, "columns": df.columns.tolist(), "numeric": numeric_cols, "categorical": categorical_cols}
