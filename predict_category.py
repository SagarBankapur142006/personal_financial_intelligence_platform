import pickle
from sentence_transformers import SentenceTransformer

model = SentenceTransformer("all-MiniLM-L6-v2")

with open("expense_model.pkl", "rb") as f:
    classifier = pickle.load(f)


def predict_category(text):

    embedding = model.encode([text])

    prediction = classifier.predict(embedding)

    return prediction[0]


print(predict_category("Dinner at restaurant"))
print(predict_category("Uber ride to airport"))
print(predict_category("Monthly Netflix payment"))
print(predict_category("Bought vegetables from market"))