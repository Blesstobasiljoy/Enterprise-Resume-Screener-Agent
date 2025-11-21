# 👔 AutoHR: Intelligent Recruitment Agent

![Python](https://img.shields.io/badge/Python-3.10%2B-blue)
![Gemini](https://img.shields.io/badge/AI-Gemini%202.5%20Flash-orange)
![Streamlit](https://img.shields.io/badge/App-Streamlit-red)

## 📖 Project Overview
**AutoHR** is a sequential multi-agent system designed to automate the initial screening phase of recruitment. It reads PDF resumes, evaluates candidates against job descriptions using reasoning, and autonomously drafts the appropriate response email.

This project was built for the **Kaggle Agents Intensive Capstone (Enterprise Track)**.

## 🤖 Agentic Architecture
The system utilizes a **Sequential Multi-Agent** pattern:

1.  **Tool Layer (The Eyes):** A custom Python-based PDF parser extracts raw text from uploaded resume files.
2.  **Evaluator Agent (The Brain):** Analyzes the extracted text against the Job Description. It acts as a reasoning engine to assign a "Match Score" (0-100) and provide a justification.
3.  **Communicator Agent (The Voice):** Conditionally operates based on the Evaluator's output.
    * *If Score > 60:* Drafts an Interview Invitation.
    * *If Score < 60:* Drafts a Polite Rejection.

## 🛠️ Tech Stack
* **Model:** Google Gemini 2.5 Flash
* **Framework:** Streamlit (Frontend), Google GenAI SDK (Agents)
* **Tools:** `pypdf` for file processing
* **Observability:** Built-in Streamlit status logging

## 🚀 How to Run Locally

1.  **Clone the repository:**
    ```bash
    git clone [https://github.com/Blesstobasiljoy/Enterprise-Resume-Screener-Agent.git](https://github.com/Blesstobasiljoy/Enterprise-Resume-Screener-Agent.git)
    cd Enterprise-Resume-Screener-Agent
    ```

2.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

3.  **Run the app:**
    ```bash
    streamlit run app.py
    ```

4.  **Enter your API Key:**
    The app requires a Google Gemini API Key (Get one from Google AI Studio).

## 📄 License
MIT License
