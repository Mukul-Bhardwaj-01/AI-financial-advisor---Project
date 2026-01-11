"""
AI Analysis Module
Integrates Groq AI for financial analysis and chat functionality.
"""

import os
from groq import Groq

# Global Groq client (initialized lazily)
_client = None


def get_client():
    """
    Initialize and return Groq client.
    Returns None if API key is not available.
    """
    global _client

    if _client is not None:
        return _client

    api_key = os.getenv("GROQ_API_KEY")
    if not api_key:
        return None

    try:
        _client = Groq(api_key=api_key)
        return _client
    except Exception as e:
        print(f"Groq initialization error: {e}")
        return None


def analyze_finances(financial_data):
    """
    Analyze financial data and provide personalized advice.
    Falls back to rule-based analysis if AI is unavailable.
    """
    try:
        client = get_client()

        if client is None:
            return get_rule_based_analysis(financial_data)

        income = financial_data.get("income", 0)
        expenses = financial_data.get("expenses", {})
        savings = financial_data.get("savings", 0)
        savings_rate = financial_data.get("savings_rate", 0)

        prompt = f"""
You are a professional financial advisor. Analyze the following financial data and provide personalized advice.

**Financial Summary:**
- Monthly Income: ₹{income:,.2f}
- Total Expenses: ₹{financial_data.get('total_expenses', 0):,.2f}
- Monthly Savings: ₹{savings:,.2f}
- Savings Rate: {savings_rate:.2f}%

**Expense Breakdown:**
"""

        for category, amount in expenses.items():
            if amount > 0:
                percentage = (amount / income * 100) if income > 0 else 0
                prompt += f"- {category}: ₹{amount:,.2f} ({percentage:.1f}% of income)\n"

        prompt += """

Please provide:
1. **Overall Financial Health Assessment** (2-3 sentences)
2. **Top 3 Specific Recommendations** (actionable advice)
3. **Warning Signs** (if any concerning patterns)
4. **Positive Highlights** (what they're doing well)

Keep the tone friendly, professional, and encouraging.
Use Indian financial context and currency (₹).
"""

        completion = client.chat.completions.create(
            messages=[
                {
                    "role": "system",
                    "content": (
                        "You are an expert financial advisor specializing in "
                        "personal finance for Indian households. Provide practical, "
                        "actionable advice."
                    ),
                },
                {"role": "user", "content": prompt},
            ],
            model="llama-3.1-8b-instant",
            temperature=0.7,
            max_tokens=1500,
        )

        return completion.choices[0].message.content

    except Exception as e:
        print(f"AI analysis error: {e}")
        return get_rule_based_analysis(financial_data)


def chat_with_ai(user_message, financial_data):
    """
    Interactive AI chat for financial queries.
    """
    try:
        client = get_client()

        if client is None:
            return (
                "AI chat is currently unavailable. "
                "Please configure the GROQ_API_KEY to enable this feature."
            )

        income = financial_data.get("income", 0)
        savings = financial_data.get("savings", 0)
        expenses = financial_data.get("expenses", {})

        context = f"""
User Financial Context:
- Monthly Income: ₹{income:,.2f}
- Monthly Savings: ₹{savings:,.2f}
- Key Expenses: {', '.join([f"{k}: ₹{v:,.0f}" for k, v in expenses.items() if v > 0])}

User Question:
{user_message}
"""

        completion = client.chat.completions.create(
            messages=[
                {
                    "role": "system",
                    "content": (
                        "You are a friendly financial advisor chatbot. "
                        "Answer questions about budgeting, savings, and investments "
                        "using Indian context and ₹ currency. Be concise and practical."
                    ),
                },
                {"role": "user", "content": context},
            ],
            model="llama-3.1-8b-instant",
            temperature=0.8,
            max_tokens=800,
        )

        return completion.choices[0].message.content

    except Exception as e:
        print(f"Chat error: {e}")
        return (
            "I'm having trouble responding right now. "
            "Please try again in a moment."
        )


def get_rule_based_analysis(financial_data):
    """
    Rule-based fallback financial analysis.
    """
    income = financial_data.get("income", 0)
    expenses = financial_data.get("expenses", {})
    savings = financial_data.get("savings", 0)
    savings_rate = financial_data.get("savings_rate", 0)

    analysis = "## 📊 Financial Analysis Report\n\n"

    analysis += "### Overall Financial Health\n\n"
    if savings_rate >= 20:
        analysis += f"Excellent! You're saving {savings_rate:.1f}% of your income.\n\n"
    elif savings_rate >= 10:
        analysis += f"Good job! You're saving {savings_rate:.1f}% of your income. Aim for 20%.\n\n"
    elif savings_rate > 0:
        analysis += f"You're saving {savings_rate:.1f}% of your income. Try increasing this.\n\n"
    else:
        analysis += "⚠️ You're currently not saving. Consider reducing expenses.\n\n"

    analysis += "### Key Recommendations\n\n"
    recommendations = []

    emi = expenses.get("EMI", 0)
    if emi and income:
        emi_pct = (emi / income) * 100
        if emi_pct > 40:
            recommendations.append(
                f"Reduce EMI burden: EMI is {emi_pct:.1f}% of income."
            )

    if savings_rate < 20 and income:
        recommendations.append(
            "Increase savings gradually to reach at least 20% of income."
        )

    for i, rec in enumerate(recommendations[:3], 1):
        analysis += f"{i}. {rec}\n"

    analysis += "\n### Positive Highlights\n\n"
    if savings > 0:
        analysis += f"- You save ₹{savings:,.0f} every month — great discipline!\n"
    else:
        analysis += "- Tracking your finances is a great first step.\n"

    return analysis