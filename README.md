# 🛡️ CYBERPULSE_v2

## 📌 Overview

**CyberPulse v2** is a Python-based **Flask web** application designed to help **small and medium-sized** **organizations** monitor their infrastructure and perform basic security assessments.

Developed as part of the **Open Innovation Project (2024–2026)**, CyberPulse provides a **centralized security dashboard** with automated scans, visual analytics, user management, and an integrated local AI security assistant powered by a self-hosted **LLM**.

The project is primarily intended for:

- **TPE / PME**
- **IT service providers**
- **Educational and research environments**

---

## 🚀 Key Features

### 🔍 Security Modules

- **Local Network Scanning**
Discover devices on the local network and identify basic characteristics.

- **Subdomain Enumeration**
Identify publicly exposed subdomains of a target domain.

- **Directory Enumeration**
Detect accessible directories on web servers.

- **NSLookup / WHOIS**
Retrieve DNS and domain registration information.

### 🧠 AI Security Operator

- Integrated local LLM (via Ollama)

- Acts as a cybersecurity assistant

- Can:

  - Explain scan results
  - Provide security insights
  - Safely trigger internal scanning modules

- No cloud dependency — 100% local

### 📊 Dashboard & Analytics

- Real-time charts and statistics
- Scan history and alerts
- Login history and audit trail

### 👥 User Management

- Authentication system
- Role-based access (admin / user)
- Profile and settings management

### 📄 Reporting

- Export scan results and dashboards as PDF reports

---

## 🧩 Project Modules

- Local Network Scanner
- Subdomain Enumerator
- Directory Enumerator
- NSLookup / WHOIS
- AI Operator (LLM-powered, sandboxed tool execution)

---

## Installation


1. Clone the folder
```
git clone https://github.com/W4RSH3LL/CYBERPULSE_v2.git
cd CYBERPULSE_v2\
```

2. Initialize the Database
```
python3 init_db.py
```

3. Using Ollama
```
ollama serve
ollama pull qwen2.5
```

4. Run the LLM model
```
ollama run qwen2.5
```

5. Build and run the Docker Compose
```
sudo docker compose --profile linux up --build
```

6. Access the Web UI at:
```
http://<your-ip>:5000
http://localhost:5000
```

7. Login with the default credentials : admin:admin123

---

## Technologies
- Python 3
- Flask
- SQLite
- Docker & Docker Compose
- Ollama (Local LLM runtime) (Qwen2.5)
- Bootstrap / Chart.js
- ReportLab (PDF export)


---

## Disclaimer

### ⚠️ Legal & Ethical Notice

This project is intended for educational and authorized use only.

### ❌ Do NOT run scans on networks, systems, or domains without explicit authorization.
Unauthorized scanning may be illegal and unethical.

The authors take no responsibility for misuse of this software.

---

## 🎓 Academic Context

This project was developed as part of the Open Innovation program (2024–2026)
and serves as a proof-of-concept security monitoring platform combining classic security tooling with modern AI-assisted analysis.
