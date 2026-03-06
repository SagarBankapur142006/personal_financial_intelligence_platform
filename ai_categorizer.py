import pickle
from sentence_transformers import SentenceTransformer

# load embedding model
embedding_model = SentenceTransformer("all-MiniLM-L6-v2")

# load trained classifier
with open("expense_model.pkl", "rb") as f:
    classifier = pickle.load(f)


def predict_category(text):
    embedding = embedding_model.encode([text])
    prediction = classifier.predict(embedding)
    return prediction[0]


def categorize_transactions(transactions):

    for txn in transactions:

        description = txn.get("merchant", "")

        txn["category"] = predict_category(description)

    return transactions