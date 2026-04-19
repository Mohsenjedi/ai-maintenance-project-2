Build a complete AI-powered web application using Python and Streamlit.

Project Title:
AI Predictive Maintenance System

Goal:
The system should analyze uploaded industrial sensor data, detect anomalies using machine learning, identify potential failure types using a knowledge base (RAG), and generate an AI-based maintenance report.

-----------------------------------

1. USER INPUT
- Allow user to upload a CSV file
- Display preview of the dataset (first rows)

-----------------------------------

2. SENSOR DATA PROCESSING
- If dataset does not include required features, simulate:
  - vibration (0–1 range)
  - temperature (0–1 range)
  - rpm (800–2000)

-----------------------------------

3. MACHINE LEARNING (ANOMALY DETECTION)
- Use Isolation Forest
- Features:
  - vibration
  - temperature
- Output:
  - anomaly label (Normal / Anomaly)
- Calculate anomaly ratio

- Display:
  - table with results
  - system risk level:
    - HIGH (red)
    - MEDIUM (yellow)
    - LOW (green)

-----------------------------------

4. RAG (RETRIEVAL AUGMENTED GENERATION)
Create a rule-based knowledge system:

Rules:
- If anomaly_ratio > 0.3 → critical_failure
- If vibration > 0.7 and temperature > 0.7 → bearing_failure
- If temperature > 0.7 → overheating
- If vibration > 0.7 → imbalance
- Else → normal

Each case must return:
- type
- cause
- solution

Display RAG result clearly.

-----------------------------------

5. AI INSIGHT ENGINE (LLM)
- Use Google Gemini API (or placeholder)
- Generate explanation including:
  - risk level
  - system condition
  - recommended action
  - short summary

-----------------------------------

6. SMART FALLBACK SYSTEM (IMPORTANT)
If AI fails:
- Generate a structured explanation manually
- Include:
  - sensor averages
  - detected issue
  - risk level
  - recommendation

Make it look like AI output (clean formatted text)

-----------------------------------

7. UI DESIGN (IMPORTANT)
- Use Streamlit
- Add header section with 4 industrial images
- Use columns for layout
- Use emojis for sections:
  - Data preview
  - ML detection
  - RAG
  - AI insight
- Color-coded alerts (error/warning/success)

-----------------------------------

8. OUTPUT
- Show:
  - Data preview
  - ML results
  - Risk status
  - RAG result
  - AI report

-----------------------------------

9. PDF EXPORT
- Generate a downloadable PDF report
- Include AI explanation text

-----------------------------------

10. REQUIREMENTS
- Code must be clean and modular
- Use functions for each part
- Handle errors gracefully
- Do not crash if API fails

-----------------------------------

Final Output:
A fully working Streamlit web app that demonstrates an end-to-end AI system combining:
- Machine Learning
- Rule-based reasoning (RAG)
- LLM explanation
- Robust fallback mechanism
- Clean UI

-----------------------------------