import os
import sqlite3
from datetime import datetime
from io import BytesIO

from flask import (
    Flask, render_template, request,
    redirect, url_for, jsonify, send_file
)
from flask_login import (
    LoginManager, UserMixin,
    login_user, login_required,
    logout_user, current_user
)
from werkzeug.security import check_password_hash, generate_password_hash

# Modules
from Modules.network_scanner import NetworkScanner
from Modules.subdomain_enum import SubdomainEnumerator
from Modules.directory_enum import DirectoryEnumerator
from Modules.nslookup_whois import NslookupWhois

from llm_tools import TOOLS

# ------------------------
# Flask / DB setup
# ------------------------
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "auth.db")

app = Flask(__name__)
app.secret_key = "school_project_secret"

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"

scan_history = []
login_history = []

# ------------------------
# User model
# ------------------------
class User(UserMixin):
    def __init__(self, id, username, role):
        self.id = id
        self.username = username
        self.role = role


@login_manager.user_loader
def load_user(user_id):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT id, username, role FROM users WHERE id=?", (user_id,))
    row = c.fetchone()
    conn.close()
    return User(*row) if row else None

# ------------------------
# Authentication
# ------------------------
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        c.execute(
            "SELECT id, password, role FROM users WHERE username=?",
            (username,)
        )
        row = c.fetchone()
        conn.close()

        if row and check_password_hash(row[1], password):
            login_user(User(row[0], username, row[2]))
            login_history.append({
                "username": username,
                "time": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            })
            return redirect(url_for("dashboard"))

    return render_template("login.html")


@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("login"))

# ------------------------
# Helper: Risk Score
# ------------------------
def calculate_risk(alerts, device_stats):
    alert_score = min(len(alerts) * 10, 50)
    device_score = min(sum(device_stats.values()), 50)
    return alert_score + device_score

# ------------------------
# Dashboard
# ------------------------
@app.route("/", methods=["GET", "POST"])
@login_required
def dashboard():
    net = NetworkScanner()
    hosts = net.run()

    scan_history.append({
        "name": net.name,
        "time": net.timestamp.strftime("%H:%M:%S")
    })

    device_stats = {"computer": 0, "phone": 0, "printer": 0, "iot": 0}
    for h in hosts:
        device_stats[h["type"]] += 1
        h.setdefault("mac", "Unknown")
        h.setdefault("status", "Active")

    subdomains = []
    directories = []
    nslookup_results = []

    if request.method == "POST":
        if request.form.get("domain"):
            s = SubdomainEnumerator(request.form["domain"])
            subdomains = s.run()
            scan_history.append({"name": s.name, "time": s.timestamp.strftime("%H:%M:%S")})

        if request.form.get("url"):
            d = DirectoryEnumerator(request.form["url"])
            directories = d.run()
            scan_history.append({"name": d.name, "time": d.timestamp.strftime("%H:%M:%S")})

        if request.form.get("ns_target"):
            n = NslookupWhois(request.form["ns_target"])
            nslookup_results = n.run()
            scan_history.append({"name": n.name, "time": n.timestamp.strftime("%H:%M:%S")})

    scan_counts = {}
    for entry in scan_history[-20:]:
        scan_counts[entry["time"]] = scan_counts.get(entry["time"], 0) + 1

    return render_template(
        "dashboard.html",
        hosts=hosts,
        device_stats=device_stats,
        subdomains=subdomains,
        directories=directories,
        nslookup_results=nslookup_results,
        alerts=net.alerts,
        history=scan_history[-10:],
        login_history=login_history[-10:],
        scan_chart_labels=list(scan_counts.keys()),
        scan_chart_values=list(scan_counts.values())
    )

# ------------------------
# 🧠 AI CHAT API (WITH STATUS)
# ------------------------
@app.route("/api/chat", methods=["POST"])
@login_required
def chat_api():
    message = request.json.get("message", "").strip().lower()

    if not message:
        return jsonify({"status": "error", "reply": "Please enter a command."})

    words = message.split()
    target = None
    for w in words:
        if "." in w or w.replace(".", "").isdigit():
            target = w
            break

    for keyword, func in TOOLS.items():
        if keyword in message:
            print(f"[SCAN] Starting {keyword} scan on {target}")
            try:
                result = func(target) if target else func()
                scan_history.append({
                    "name": keyword,
                    "time": datetime.now().strftime("%H:%M:%S")
                })
                return jsonify({
                    "status": "done",
                    "tool": keyword,
                    "reply": result
                })
            except Exception as e:
                return jsonify({"status": "error", "reply": str(e)})

    return jsonify({
        "status": "error",
        "reply": (
            "Unknown command.\n\n"
            "Available commands:\n"
            "- directory <url>\n"
            "- subdomain <domain>\n"
            "- network scan\n"
            "- nslookup <domain>\n"
            "- whois <domain>\n"
            "- dns <domain>"
        )
    })

# ------------------------
# PDF Export
# ------------------------
@app.route("/export_pdf")
@login_required
def export_pdf():
    net = NetworkScanner()
    hosts = net.run()

    device_stats = {"computer": 0, "phone": 0, "printer": 0, "iot": 0}
    for h in hosts:
        device_stats[h["type"]] += 1
        h.setdefault("mac", "Unknown")
        h.setdefault("status", "Active")

    risk_score = calculate_risk(net.alerts, device_stats)

    from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
    from reportlab.lib.pagesizes import A4
    from reportlab.lib.styles import getSampleStyleSheet
    from reportlab.lib import colors
    from reportlab.graphics.shapes import Drawing
    from reportlab.graphics.charts.barcharts import VerticalBarChart

    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=A4)
    styles = getSampleStyleSheet()
    elements = []

    elements.append(Paragraph("🛡️ Network Defense Dashboard Report", styles["Title"]))
    elements.append(Spacer(1, 12))
    elements.append(Paragraph(f"Analyst: {current_user.username}", styles["Normal"]))
    elements.append(Paragraph(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}", styles["Normal"]))
    elements.append(Spacer(1, 20))

    elements.append(Paragraph("🧠 Risk Score", styles["Heading2"]))
    elements.append(Paragraph(f"<b>{risk_score} / 100</b>", styles["Normal"]))
    elements.append(Spacer(1, 20))

    table_data = [["IP", "Hostname", "Type", "MAC", "Status"]]
    for h in hosts:
        table_data.append([h["ip"], h["hostname"], h["type"], h["mac"], h["status"]])

    table = Table(table_data)
    table.setStyle(TableStyle([
        ("BACKGROUND", (0,0), (-1,0), colors.HexColor("#2563eb")),
        ("TEXTCOLOR", (0,0), (-1,0), colors.white),
        ("GRID", (0,0), (-1,-1), 0.5, colors.grey),
    ]))
    elements.append(table)

    drawing = Drawing(400, 200)
    chart = VerticalBarChart()
    chart.data = [[device_stats[k] for k in device_stats]]
    chart.categoryAxis.categoryNames = list(device_stats.keys())
    chart.width = 300
    chart.height = 125
    chart.x = 50
    chart.y = 50
    drawing.add(chart)
    elements.append(drawing)

    doc.build(elements)
    buffer.seek(0)

    return send_file(
        buffer,
        as_attachment=True,
        download_name="dashboard_report.pdf",
        mimetype="application/pdf"
    )

# ------------------------
# Settings
# ------------------------
@app.route("/settings", methods=["GET", "POST"])
@login_required
def settings():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()

    if request.method == "POST":
        if current_user.role == "admin" and request.form.get("new_username"):
            c.execute(
                "INSERT INTO users (username, password, role) VALUES (?, ?, ?)",
                (
                    request.form["new_username"],
                    generate_password_hash(request.form["new_password"]),
                    request.form["role"]
                )
            )

        if request.form.get("update_username"):
            new_name = request.form["update_username"]
            c.execute("UPDATE users SET username=? WHERE id=?", (new_name, current_user.id))
            current_user.username = new_name

        conn.commit()
    conn.close()
    return render_template("settings.html")

# ------------------------
# Profile
# ------------------------
@app.route("/profile")
@login_required
def profile():
    return render_template("profile.html")

# ------------------------
# Run app
# ------------------------
if __name__ == "__main__":
    app.run(debug=True)
