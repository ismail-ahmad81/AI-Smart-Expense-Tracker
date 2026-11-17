import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import make_pipeline


def train_categorizer():
    training_texts = [
        "Zomato food order", "Swiggy dinner", "Burger King lunch", "Grocery shopping",
        "Uber ride", "Petrol pump refill", "Metro card recharge", "Ola cab",
        "Netflix subscription", "Amazon Prime", "Movie ticket",
        "Electricity bill", "Wifi bill recharge", "Tuition fees paid"
    ]
    training_labels = [
        "Food", "Food", "Food", "Food",
        "Travel", "Travel", "Travel", "Travel",
        "Entertainment", "Entertainment", "Entertainment",
        "Bills", "Bills", "Bills"
    ]
    
    model = make_pipeline(TfidfVectorizer(), MultinomialNB())
    model.fit(training_texts, training_labels)
    return model

ai_model = train_categorizer()

def predict_category(text):
    try:
        return ai_model.predict([text])[0]
    except:
        return "General"

def check_budget_status(monthly_budget, total_spent_so_far, current_day):
    total_days = 30
    daily_avg = total_spent_so_far / current_day if current_day > 0 else 0
    predicted_total = daily_avg * total_days
    
    remaining_budget = monthly_budget - total_spent_so_far
    remaining_days = total_days - current_day
    safe_daily_limit = remaining_budget / remaining_days if remaining_days > 0 else 0

    if predicted_total > monthly_budget:
        return {
            "status": "ALERT",
            "message": f"Spending speed fast hai! Roz ka max ₹{round(safe_daily_limit, 2)} hi kharch karein.",
            "predicted_total": round(predicted_total, 2)
        }
    return {
        "status": "SAFE",
        "message": "Aapka budget control me hai.",
        "predicted_total": round(predicted_total, 2)
    }