from fastapi import FastAPI
import joblib
import pandas as pd

from database import get_connection

app = FastAPI(title="Credit Card Fraud Detection API")

# Load trained model and scaler
model = joblib.load("../models/fraud_detection_model.pkl")
scaler = joblib.load("../models/amount_scaler.pkl")


@app.get("/")
def home():
    return {
        "message": "Credit Card Fraud Detection API is running"
    }


@app.post("/predict")
def predict_transaction(transaction: dict):

    # Convert transaction into DataFrame
    data = pd.DataFrame([transaction])

    # Scale Amount
    data["Amount"] = scaler.transform(data[["Amount"]])

    # Make prediction
    prediction = model.predict(data)[0]
    probability = model.predict_proba(data)[0][1]

    result = "Fraud" if prediction == 1 else "Normal"

    # Save prediction to PostgreSQL
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        INSERT INTO transactions (
            transaction_time,
            amount,
            prediction,
            fraud_probability
        )
        VALUES (%s, %s, %s, %s)
        """,
        (
            transaction["Time"],
            transaction["Amount"],
            result,
            float(probability)
        )
    )

    conn.commit()

    cursor.close()
    conn.close()

    return {
        "prediction": result,
        "fraud_probability": round(float(probability), 4)
    }

@app.get("/transactions")
def get_transactions():

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT
            id,
            transaction_time,
            amount,
            prediction,
            fraud_probability,
            created_at
        FROM transactions
        ORDER BY id DESC
        LIMIT 20
        """
    )

    rows = cursor.fetchall()

    cursor.close()
    conn.close()

    transactions = []

    for row in rows:
        transactions.append({
            "id": row[0],
            "transaction_time": row[1],
            "amount": row[2],
            "prediction": row[3],
            "fraud_probability": row[4],
            "created_at": str(row[5])
        })

    return {
        "transactions": transactions
    }