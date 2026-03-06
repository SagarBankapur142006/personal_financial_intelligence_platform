from collections import defaultdict
from datetime import datetime

# categories that are optional spending
DISCRETIONARY = {
    "Food",
    "Entertainment",
    "Shopping"
}

# essential categories
ESSENTIAL = {
    "Bills",
    "Groceries",
    "Health",
    "Transport"
}


def calculate_metrics(transactions):

    if not transactions:
        return _empty_metrics()

    total_spent = sum(float(t["amount"]) for t in transactions)

    category_spending = defaultdict(float)

    for t in transactions:
        category_spending[t["category"]] += float(t["amount"])

    category_spending = dict(category_spending)

    # determine time range
    try:
        dates = [datetime.strptime(t["date"], "%Y-%m-%d") for t in transactions]
        days = max((max(dates) - min(dates)).days, 1)
    except:
        days = 30

    daily_avg = total_spent / days
    yearly_projection = round(daily_avg * 365, 2)

    top_category = max(category_spending, key=category_spending.get)

    health_score = _calculate_health_score(total_spent, category_spending)

    insights = _generate_insights(
        total_spent,
        category_spending,
        yearly_projection,
        daily_avg,
        top_category
    )

    return {
        "total_spent": round(total_spent, 2),
        "yearly_spending_projection": yearly_projection,
        "daily_average": round(daily_avg, 2),
        "financial_health_score": health_score,
        "category_spending": category_spending,
        "top_category": top_category,
        "insights": insights
    }


def _calculate_health_score(total_spent, category_spending):

    score = 100

    discretionary_total = sum(
        v for k, v in category_spending.items() if k in DISCRETIONARY
    )

    if total_spent > 0:
        ratio = discretionary_total / total_spent

        if ratio > 0.6:
            score -= 40
        elif ratio > 0.45:
            score -= 25
        elif ratio > 0.30:
            score -= 10

    transport_spend = category_spending.get("Transport", 0)

    if total_spent > 0:
        transport_ratio = transport_spend / total_spent

        if transport_ratio > 0.35:
            score -= 15

    return max(10, min(score, 100))


def _generate_insights(total_spent, category_spending, yearly_projection, daily_avg, top_category):

    insights = []

    top_amount = category_spending[top_category]
    top_pct = round((top_amount / total_spent) * 100, 1)

    insights.append(
        f"Your largest spending category is {top_category} at ₹{top_amount:,.0f} ({top_pct}% of total expenses)."
    )

    discretionary_total = sum(
        v for k, v in category_spending.items() if k in DISCRETIONARY
    )

    discretionary_pct = round((discretionary_total / total_spent) * 100, 1)

    if discretionary_pct > 50:
        insights.append(
            f"⚠️ Discretionary spending is high at {discretionary_pct}%. Reducing dining and shopping could significantly improve savings."
        )
    elif discretionary_pct > 35:
        insights.append(
            f"Discretionary expenses make up {discretionary_pct}% of spending. Consider trimming optional purchases."
        )
    else:
        insights.append(
            f"Good discipline: only {discretionary_pct}% of your spending is discretionary."
        )

    transport_spend = category_spending.get("Transport", 0)

    if transport_spend > total_spent * 0.30:
        insights.append(
            "🚕 Transport spending is relatively high. Using public transport occasionally could reduce costs."
        )

    potential_savings = discretionary_total * 0.20

    if potential_savings > 0:
        insights.append(
            f"💡 Reducing discretionary spending by 20% could save approximately ₹{potential_savings:,.0f}."
        )

    insights.append(
        f"At your current pace, you are projected to spend around ₹{yearly_projection:,.0f} this year."
    )

    insights.append(
        f"Your average daily spending is ₹{daily_avg:,.0f}."
    )

    return insights


def _empty_metrics():

    return {
        "total_spent": 0,
        "yearly_spending_projection": 0,
        "daily_average": 0,
        "financial_health_score": 0,
        "category_spending": {},
        "top_category": "N/A",
        "insights": ["No transactions to analyze."]
    }