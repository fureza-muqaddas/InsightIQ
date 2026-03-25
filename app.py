import os
import json
from flask import Flask, render_template, request, jsonify, redirect, url_for, session
from werkzeug.utils import secure_filename
import pandas as pd
from config import Config
from database.models import init_db, Session, UploadedFile, ChatHistory, Report
from agent.analyst import chat_with_data, generate_report, generate_chart_data, load_dataframe, get_data_summary

app = Flask(__name__)
app.config.from_object(Config)
app.secret_key = Config.SECRET_KEY

os.makedirs(Config.UPLOAD_FOLDER, exist_ok=True)
os.makedirs("database", exist_ok=True)
init_db()

def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in Config.ALLOWED_EXTENSIONS

@app.route("/")
def index():
    db = Session()
    files = db.query(UploadedFile).order_by(UploadedFile.uploaded_at.desc()).all()
    db.close()
    return render_template("index.html", files=files)

@app.route("/upload", methods=["POST"])
def upload_file():
    if "file" not in request.files:
        return jsonify({"error": "No file selected"}), 400
    
    file = request.files["file"]
    if file.filename == "" or not allowed_file(file.filename):
        return jsonify({"error": "Invalid file type. Use CSV, Excel, or JSON."}), 400

    filename = secure_filename(file.filename)
    filepath = os.path.join(Config.UPLOAD_FOLDER, filename)
    file.save(filepath)

    try:
        df = load_dataframe(filepath)
        summary = get_data_summary(df)

        db = Session()
        uploaded = UploadedFile(
            filename=filename,
            original_name=file.filename,
            file_type=filename.rsplit(".", 1)[1].lower(),
            row_count=len(df),
            col_count=len(df.columns),
            summary=summary,
        )
        db.add(uploaded)
        db.commit()
        file_id = uploaded.id
        db.close()

        return jsonify({"success": True, "file_id": file_id, "rows": len(df), "columns": len(df.columns)})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/analyze/<int:file_id>")
def analyze(file_id):
    db = Session()
    file = db.query(UploadedFile).filter_by(id=file_id).first()
    if not file:
        db.close()
        return redirect(url_for("index"))
    
    chat_msgs = db.query(ChatHistory).filter_by(file_id=file_id).order_by(ChatHistory.created_at).all()
    db.close()
    
    filepath = os.path.join(Config.UPLOAD_FOLDER, file.filename)
    chart_data = generate_chart_data(filepath)
    summary = json.loads(file.summary) if file.summary else {}
    
    return render_template("chat.html", file=file, chart_data=json.dumps(chart_data), 
                           chat_history=chat_msgs, summary=summary)

@app.route("/chat/<int:file_id>", methods=["POST"])
def chat(file_id):
    db = Session()
    file = db.query(UploadedFile).filter_by(id=file_id).first()
    if not file:
        db.close()
        return jsonify({"error": "File not found"}), 404

    user_message = request.json.get("message", "")
    if not user_message:
        db.close()
        return jsonify({"error": "Empty message"}), 400

    history = db.query(ChatHistory).filter_by(file_id=file_id).order_by(ChatHistory.created_at).all()
    messages = [{"role": h.role, "content": h.message} for h in history]

    filepath = os.path.join(Config.UPLOAD_FOLDER, file.filename)
    
    try:
        response = chat_with_data(filepath, messages, user_message)
        
        db.add(ChatHistory(file_id=file_id, role="user", message=user_message))
        db.add(ChatHistory(file_id=file_id, role="assistant", message=response))
        db.commit()
        db.close()
        
        return jsonify({"response": response})
    except Exception as e:
        db.close()
        return jsonify({"error": str(e)}), 500

@app.route("/report/<int:file_id>", methods=["GET", "POST"])
def report(file_id):
    db = Session()
    file = db.query(UploadedFile).filter_by(id=file_id).first()
    if not file:
        db.close()
        return redirect(url_for("index"))

    if request.method == "POST":
        filepath = os.path.join(Config.UPLOAD_FOLDER, file.filename)
        try:
            report_data = generate_report(filepath)
            new_report = Report(
                file_id=file_id,
                title=f"Analysis Report — {file.original_name}",
                content=report_data["full_report"],
            )
            db.add(new_report)
            db.commit()
            report_id = new_report.id
            db.close()
            return jsonify({"success": True, "report_id": report_id, "content": report_data["full_report"]})
        except Exception as e:
            db.close()
            return jsonify({"error": str(e)}), 500

    existing = db.query(Report).filter_by(file_id=file_id).order_by(Report.created_at.desc()).first()
    db.close()
    return render_template("report.html", file=file, report=existing)

@app.route("/delete/<int:file_id>", methods=["DELETE"])
def delete_file(file_id):
    db = Session()
    file = db.query(UploadedFile).filter_by(id=file_id).first()
    if file:
        filepath = os.path.join(Config.UPLOAD_FOLDER, file.filename)
        if os.path.exists(filepath):
            os.remove(filepath)
        db.query(ChatHistory).filter_by(file_id=file_id).delete()
        db.query(Report).filter_by(file_id=file_id).delete()
        db.delete(file)
        db.commit()
    db.close()
    return jsonify({"success": True})

if __name__ == "__main__":
    app.run(debug=True)