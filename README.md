# 🛡️ SafeOps LogMiner - Intelligent DevSecOps Pipeline

> **A Next-Generation Security Intelligence Platform designed to Collect, Analyze, and Remediate Vulnerabilities in Real-Time.**

![Project Status](https://img.shields.io/badge/status-active-success.svg)
![License](https://img.shields.io/badge/license-MIT-blue.svg)
![Docker](https://img.shields.io/badge/docker-%230db7ed.svg?style=flat&logo=docker&logoColor=white)
![React](https://img.shields.io/badge/react-%2320232a.svg?style=flat&logo=react&logoColor=%2361DAFB)
![Python](https://img.shields.io/badge/python-3670A0?style=flat&logo=python&logoColor=ffdd54)
![NodeJS](https://img.shields.io/badge/node.js-6DA55F?style=flat&logo=node.js&logoColor=white)

## 📖 Overview

**SafeOps LogMiner** is a comprehensive DevSecOps solution that bridges the gap between CI/CD log data and actionable security insights. By leveraging advanced AI models and a microservices architecture, it automates the detection of security vulnerabilities within your build pipelines and suggests intelligent fixes, all visualized through a premium real-time dashboard.

## 🎥 Demo

![Demo Video](https://github.com/user-attachments/assets/placeholder-video-link)
*(Replace this link with your actual demo video or GIF)*

## 🚀 Key Features

*   **🔍 Centralized Log Collection**: Seamlessly ingests logs from major CI/CD platforms (GitHub Actions, GitLab CI, Jenkins).
*   **🧠 AI-Powered Analysis**: Utilizes Google Gemini models to detect complex vulnerabilities (SQL Injection, XSS, Secrets Leaks) that traditional scanners might miss.
*   **💡 Intelligent Fix Suggestions**: Automatically generates code patches and remediation advice for detected issues.
*   **📊 Real-Time Dashboard**: A stunning, responsive React UI for monitoring pipeline health, vulnerability trends, and system status.
*   **📑 Automated Reporting**: Generates detailed PDF security reports for compliance and auditing.
*   **⚡ Event-Driven Architecture**: Built on RabbitMQ and Redis for high-performance, asynchronous data processing.

## 🏗️ Architecture & Microservices

The solution is composed of several specialized microservices, fully containerized for easy deployment:

| Service | Technology | Description |
| :--- | :--- | :--- |
| **LogCollector** | Node.js / Express | Ingests raw logs and webhooks from CI/CD tools, storing them in MongoDB. |
| **LogParser** | Python / FastAPI | Consumes raw logs, normalizes data, and extracts relevant features for analysis. |
| **VulnDetector** | Python / FastAPI | The AI core. Analyzes parsed logs to detect security vulnerabilities and stores them in Postgres. |
| **FixSuggester** | Python / FastAPI | Listens for new vulnerabilities and prompts the LLM to generate code fixes. |
| **ReportGenerator** | Python / FastAPI | Compiles vulnerability data into professional PDF reports (stored in MinIO). |
| **Dashboard** | React / Vite | The user-facing frontend for visualization and interaction. |

### Infrastructure
*   **Databases**: PostgreSQL (Relational Data), MongoDB (Raw Logs), Redis (Caching/State).
*   **Message Broker**: RabbitMQ (Inter-service communication).
*   **Object Storage**: MinIO (Report artifacts).

## 🛠️ Tech Stack

*   **Frontend**: React 18, Vite, Tailwind CSS, Recharts, Framer Motion.
*   **Backend**: Python (FastAPI), Node.js (Express), Prism.
*   **AI/ML**: Google Gemini Pro/Flash (via API).
*   **DevOps**: Docker, Docker Compose, Nginx.
*   **Tools**: Git, Postman.

## 🏁 Getting Started

Follow these steps to get a local instance up and running.

### Prerequisites
*   [Docker Desktop](https://www.docker.com/products/docker-desktop) installed and running.
*   [Git](https://git-scm.com/downloads) installed.

### Installation

1.  **Clone the Repository**
    ```bash
    git clone https://github.com/abdelilah771/devsecops-pipeline.git
    cd devsecops-pipeline
    ```

2.  **Environment Configuration**
    Ensure you have the necessary `.env` files in each service directory.
    *(Note: The project comes with default configurations for local Docker deployment. You may need to add your `GEMINI_API_KEY` in `vulndetcteur/.env` and `FixSuggester/.env`)*.

3.  **Build and Run with Docker Compose**
    ```bash
    docker-compose up --build -d
    ```

4.  **Access the Application**
    *   **Frontend Dashboard**: [http://localhost:8080](http://localhost:8080)
    *   **LogCollector API**: [http://localhost:3000](http://localhost:3000)
    *   **LogParser docs**: [http://localhost:8001/docs](http://localhost:8001/docs)
    *   **VulnDetector docs**: [http://localhost:8002/docs](http://localhost:8002/docs)
    *   **FixSuggester docs**: [http://localhost:8003/docs](http://localhost:8003/docs)
    *   **ReportGenerator docs**: [http://localhost:8005/docs](http://localhost:8005/docs)
    *   **MinIO Console**: [http://localhost:9001](http://localhost:9001) (User: `minioadmin`, Pass: `minioadmin123`)

## 📂 Project Structure

```bash
devsecops-pipeline/
├── dashboard/          # Frontend Application (React)
├── logcollector/       # Log Ingestion Service (Node.js)
├── logparser/          # Log Parsing Service (Python)
├── vulndetcteur/       # Vulnerability Detection Service (Python/AI)
├── FixSuggester/       # Fix Generation Service (Python/AI)
├── ReportGenerator/    # Reporting Service (Python)
├── docker-compose.yml  # Main orchestration file
└── README.md           # Project Documentation
```

## 🤝 Contribution

Contributions are welcome! Please fork this repository and submit a pull request for any features, bug fixes, or enhancements.

1.  Fork the Project
2.  Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3.  Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4.  Push to the Branch (`git push origin feature/AmazingFeature`)
5.  Open a Pull Request

## 📄 License

Distributed under the MIT License. See `LICENSE` for more information.

---
*Built with ❤️ by Abdelilah & The DevSecOps Team.*
