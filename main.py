import io
import pandas as pd

from fastapi import FastAPI,UploadFile,File,HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from ai_categorizer import categorize_transactions
from analyzer import calculate_metrics


app=FastAPI(title="Finance Intelligence API")


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"]
)


REQUIRED_COLUMNS={"date","merchant","amount"}


@app.get("/")
def home():

    return {"message":"Finance Intelligence API running"}


@app.post("/analyze")
async def analyze(file:UploadFile=File(...)):

    if not file.filename.endswith(".csv"):

        raise HTTPException(400,"Upload CSV file")

    contents=await file.read()

    try:

        df=pd.read_csv(io.StringIO(contents.decode()))

    except:

        raise HTTPException(422,"Invalid CSV format")

    df.columns=[c.lower().strip() for c in df.columns]

    missing=REQUIRED_COLUMNS-set(df.columns)

    if missing:

        raise HTTPException(
            422,
            f"CSV must contain columns: date, merchant, amount"
        )

    df["amount"]=pd.to_numeric(df["amount"],errors="coerce")

    df=df.dropna()

    transactions=df[["date","merchant","amount"]].to_dict(orient="records")

    transactions=categorize_transactions(transactions)

    metrics=calculate_metrics(transactions)

    return JSONResponse({
        "status":"success",
        "transaction_count":len(transactions),
        "data":metrics
    })