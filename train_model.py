import pandas as pd
import pickle

from sentence_transformers import SentenceTransformer
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report

print("Loading dataset...")

data = pd.read_csv("transactions.csv")

# Robust date parsing (works for DD-MM-YYYY and YYYY-MM-DD)
data["date"] = pd.to_datetime(data["date"], dayfirst=True, errors="coerce")

# remove rows where date failed to parse
data = data.dropna(subset=["date"])

texts = data["description"].astype(str)
labels = data["category"]

print("Loading language model...")

model = SentenceTransformer("all-MiniLM-L6-v2")

print("Encoding text...")

X = model.encode(texts.tolist())

y = labels

print("Splitting dataset...")

X_train, X_test, y_train, y_test = train_test_split(
    X, y,
    test_size=0.2,
    random_state=42
)

print("Training classifier...")

classifier = LogisticRegression(max_iter=1000)
classifier.fit(X_train, y_train)

print("Evaluating model...\n")

predictions = classifier.predict(X_test)

print(classification_report(y_test, predictions))

print("Saving model...")

with open("expense_model.pkl", "wb") as f:
    pickle.dump(classifier, f)

print("\nModel saved as expense_model.pkl")