from sentence_transformers import SentenceTransformer
import pickle

# Load trained model
model = SentenceTransformer("all-MiniLM-L6-v2")

with open("expense_model.pkl", "rb") as f:
    clf = pickle.load(f)

# Income detection keywords
INCOME_KEYWORDS = [
    "salary",
    "credit",
    "refund",
    "payment received",
    "upi credit",
    "bonus",
    "interest",
    "transfer from",
    "bank credit",
    "deposit"
]


def detect_income(text):
    text = text.lower()

    for word in INCOME_KEYWORDS:
        if word in text:
            return True

    return False


def categorize_transaction(text):

    if detect_income(text):
        return "Income"

    embedding = model.encode([text])
    category = clf.predict(embedding)[0]

    return category