# AI Financial Advisor

An AI-powered financial advisory web application that analyzes user income and expenses to provide personalized financial insights, health scores, and actionable recommendations.

## Developed by
- **Mukul Bhardwaj** — AI Integration, Backend Development, Data Processing, and Frontend UI

## Features
- Manual financial data entry and CSV upload support
- Interactive dashboard with visual charts (Pie chart and Bar graph)
- AI-powered financial analysis using Groq LLaMA 3.1
- Real-time chat with an AI-based financial advisor
- Financial health score calculation (0–100)
- Personalized and contextual financial recommendations

## Demo
🎥 Project Demo Video (YouTube – Unlisted):  
https://youtu.be/uyfSR2vtCwU?si=-LZsEPj3kv3BwQby

## Tech Stack
- **Backend:** Flask (Python)
- **Frontend:** HTML, CSS, JavaScript
- **Data Visualization:** Chart.js
- **AI Model:** Groq LLaMA 3.1 (8B)
- **Data Processing:** Pandas

## Project Structure

ai-financial-advisor/<br>
├── app.py<br>
├── ai_analyzer.py<br>
├── data_processor.py<br>
├── requirements.txt<br>
├── vercel.json<br>
├── .env.example<br>
├── templates/<br>
├── static/<br>


## Installation & Setup

1. Clone the repository:
```bash
git clone https://github.com/Mukul-Bhardwaj-01/ai-financial-advisor.git
cd ai-financial-advisor
pip install -r requirements.txt
```

2. Create a .env file in the project root and add:
```bash
GROQ_API_KEY=your_api_key_here
FLASK_SECRET_KEY=your_secret_key_here
```

3. Run the application locally:
```bash
python app.py
```

4. Open your browser and visit:
```bash
http://127.0.0.1:5000
```

### CSV file requirements
It should contain two columns: Category and Amount.
```bash
Example:

Category,Amount
Income,50000
Rent,15000
Food,8000
Transportation,4000
```

## Deployment

The application is designed to be deployed as a serverless Flask application using Vercel with secure environment variable management.