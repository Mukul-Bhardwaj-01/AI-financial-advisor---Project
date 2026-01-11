"""
Data Processing Module
Handles CSV parsing, manual data processing, and financial calculations.
"""

import pandas as pd
from datetime import datetime

EXPENSE_CATEGORIES = [
    "Rent",
    "Food",
    "Transportation",
    "Shopping",
    "Entertainment",
    "EMI",
    "Utilities",
    "Healthcare",
    "Others",
]


def process_manual_data(data):
    """
    Process manually entered financial data.
    """
    try:
        income = float(data.get("income", 0))

        expenses = {
            category: float(data.get(category.lower(), 0))
            for category in EXPENSE_CATEGORIES
        }

        total_expenses = sum(expenses.values())
        savings = income - total_expenses
        savings_rate = (savings / income * 100) if income > 0 else 0

        expense_percentages = {
            category: round((amount / income) * 100, 2) if income > 0 else 0
            for category, amount in expenses.items()
        }

        return {
            "income": income,
            "expenses": expenses,
            "total_expenses": total_expenses,
            "savings": savings,
            "savings_rate": round(savings_rate, 2),
            "expense_percentages": expense_percentages,
            "month": data.get("month", datetime.now().strftime("%B %Y")),
            "timestamp": datetime.now().isoformat(),
            "source": "manual",
        }

    except Exception as e:
        raise Exception(f"Error processing manual data: {str(e)}")


def process_csv_data(filepath):
    """
    Process CSV file containing financial data.
    Expected format:
    Category, Amount
    """
    try:
        df = pd.read_csv(filepath)
        df.columns = df.columns.str.strip().str.lower()

        income = 0.0
        expenses = {category: 0.0 for category in EXPENSE_CATEGORIES}

        for _, row in df.iterrows():
            category = str(row.get("category", "")).strip().title()
            try:
                amount = float(row.get("amount", 0))
            except ValueError:
                amount = 0

            if category == "Income":
                income = amount
            elif category in expenses:
                expenses[category] += amount
            else:
                expenses["Others"] += amount

        total_expenses = sum(expenses.values())
        savings = income - total_expenses
        savings_rate = (savings / income * 100) if income > 0 else 0

        expense_percentages = {
            category: round((amount / income) * 100, 2) if income > 0 else 0
            for category, amount in expenses.items()
        }

        return {
            "income": income,
            "expenses": expenses,
            "total_expenses": total_expenses,
            "savings": savings,
            "savings_rate": round(savings_rate, 2),
            "expense_percentages": expense_percentages,
            "month": datetime.now().strftime("%B %Y"),
            "timestamp": datetime.now().isoformat(),
            "source": "csv",
        }

    except Exception as e:
        raise Exception(f"Error processing CSV: {str(e)}")


def calculate_financial_health(financial_data):
    """
    Calculate financial health score (0–100).
    """
    try:
        score = 0

        income = financial_data.get("income", 0)
        savings = financial_data.get("savings", 0)
        savings_rate = financial_data.get("savings_rate", 0)
        expenses = financial_data.get("expenses", {})

        # Savings rate (40 points)
        if savings_rate >= 30:
            score += 40
        elif savings_rate >= 20:
            score += 30
        elif savings_rate >= 10:
            score += 20
        elif savings_rate >= 5:
            score += 10

        # Positive savings (20 points)
        if savings > 0:
            score += 20
        elif savings >= -income * 0.1:
            score += 10

        # EMI burden (20 points)
        emi = expenses.get("EMI", 0)
        emi_pct = (emi / income * 100) if income > 0 else 0

        if emi_pct == 0:
            score += 20
        elif emi_pct <= 30:
            score += 15
        elif emi_pct <= 40:
            score += 10
        elif emi_pct <= 50:
            score += 5

        # Expense balance (20 points)
        positive_expenses = [v for v in expenses.values() if v > 0]
        if positive_expenses and income > 0:
            max_pct = (max(positive_expenses) / income) * 100
            if max_pct <= 30:
                score += 20
            elif max_pct <= 40:
                score += 15
            elif max_pct <= 50:
                score += 10
            elif max_pct <= 60:
                score += 5

        score = max(0, min(100, score))

        if score >= 80:
            status, color = "Excellent", "green"
        elif score >= 60:
            status, color = "Good", "lightgreen"
        elif score >= 40:
            status, color = "Fair", "orange"
        else:
            status, color = "Needs Improvement", "red"

        return {"score": score, "status": status, "color": color}

    except Exception:
        return {"score": 0, "status": "Error", "color": "gray"}