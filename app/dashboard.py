import streamlit as st
import requests
import pandas as pd

st.set_page_config(
    page_title="Credit Card Fraud Detection",
    page_icon="💳",
    layout="wide"
)

st.title("💳 Credit Card Fraud Detection")
st.write("AI-powered credit card transaction fraud detection")

API_URL = "http://127.0.0.1:8000"

# --------------------------------------------------
# Transaction Prediction
# --------------------------------------------------

st.divider()
st.subheader("🔍 Check a Transaction")

col1, col2 = st.columns(2)

with col1:
    transaction_time = st.number_input(
        "Transaction Time",
        min_value=0.0,
        value=10000.0
    )

with col2:
    amount = st.number_input(
        "Transaction Amount",
        min_value=0.0,
        value=50.0
    )

st.subheader("🔢 Anonymized Features")

st.info(
    "V1–V28 are anonymized features from the original "
    "credit card fraud dataset."
)

features = {}

cols = st.columns(4)

for i in range(1, 29):
    with cols[(i - 1) % 4]:
        features[f"V{i}"] = st.number_input(
            f"V{i}",
            value=0.0,
            format="%.6f"
        )

if st.button("🔍 Check Transaction", type="primary"):

    transaction = {
        "Time": transaction_time,
        "Amount": amount
    }

    transaction.update(features)

    try:
        response = requests.post(
            f"{API_URL}/predict",
            json=transaction,
            timeout=30
        )

        if response.status_code == 200:

            result = response.json()

            prediction = result["prediction"]
            probability = result["fraud_probability"]

            st.divider()

            if prediction == "Fraud":
                st.error("🚨 FRAUD TRANSACTION DETECTED")
            else:
                st.success("✅ TRANSACTION APPEARS NORMAL")

            st.metric(
                "Fraud Probability",
                f"{probability * 100:.2f}%"
            )

        else:
            st.error(
                f"API Error: {response.status_code}"
            )

    except requests.exceptions.ConnectionError:
        st.error(
            "❌ Cannot connect to FastAPI. "
            "Make sure FastAPI is running on port 8000."
        )

    except Exception as e:
        st.error(f"Error: {e}")


# --------------------------------------------------
# Transaction History
# --------------------------------------------------

st.divider()
# --------------------------------------------------
# Dashboard Statistics
# --------------------------------------------------

st.divider()
st.subheader("📊 Dashboard Statistics")

try:
    response = requests.get(
        f"{API_URL}/transactions",
        timeout=10
    )

    if response.status_code == 200:

        result = response.json()
        transactions = result["transactions"]

        if transactions:

            total_transactions = len(transactions)

            fraud_transactions = sum(
                1 for transaction in transactions
                if transaction["prediction"] == "Fraud"
            )

            normal_transactions = (
                total_transactions - fraud_transactions
            )

            average_probability = sum(
                transaction["fraud_probability"]
                for transaction in transactions
            ) / total_transactions

            col1, col2, col3, col4 = st.columns(4)

            with col1:
                st.metric(
                    "Total Transactions",
                    total_transactions
                )

            with col2:
                st.metric(
                    "Fraud Transactions",
                    fraud_transactions
                )

            with col3:
                st.metric(
                    "Normal Transactions",
                    normal_transactions
                )

            with col4:
                st.metric(
                    "Avg Fraud Probability",
                    f"{average_probability * 100:.2f}%"
                )

        else:
            st.info("No transaction statistics available yet.")

except requests.exceptions.ConnectionError:
    st.warning(
        "Start FastAPI to display dashboard statistics."
    )

except Exception as e:
    st.warning(f"Unable to load statistics: {e}")
st.subheader("📋 Recent Transaction History")

if st.button("🔄 Refresh History"):

    try:
        response = requests.get(
            f"{API_URL}/transactions",
            timeout=10
        )

        if response.status_code == 200:

            result = response.json()

            transactions = result["transactions"]

            if transactions:

                history_df = pd.DataFrame(transactions)

                history_df["fraud_probability"] = (
                    history_df["fraud_probability"] * 100
                ).round(2)

                history_df = history_df.rename(
                    columns={
                        "id": "ID",
                        "transaction_time": "Time",
                        "amount": "Amount",
                        "prediction": "Prediction",
                        "fraud_probability": "Fraud Probability (%)",
                        "created_at": "Created At"
                    }
                )

                st.dataframe(
                    history_df,
                    use_container_width=True
                )

            else:
                st.info("No transactions found.")

        else:
            st.error(
                f"API Error: {response.status_code}"
            )

    except requests.exceptions.ConnectionError:
        st.error(
            "❌ Cannot connect to FastAPI. "
            "Make sure FastAPI is running."
        )

    except Exception as e:
        st.error(f"Error: {e}")

# --------------------------------------------------
# Fraud vs Normal Chart
# --------------------------------------------------

st.divider()
st.subheader("📈 Fraud vs Normal Transactions")

try:
    response = requests.get(
        f"{API_URL}/transactions",
        timeout=10
    )

    if response.status_code == 200:

        result = response.json()
        transactions = result["transactions"]

        if transactions:

            chart_data = pd.DataFrame(
                {
                    "Transaction Type": ["Normal", "Fraud"],
                    "Count": [
                        sum(
                            1 for transaction in transactions
                            if transaction["prediction"] == "Normal"
                        ),
                        sum(
                            1 for transaction in transactions
                            if transaction["prediction"] == "Fraud"
                        )
                    ]
                }
            )

            st.bar_chart(
                chart_data.set_index("Transaction Type")
            )

        else:
            st.info("No transaction data available for the chart.")

except requests.exceptions.ConnectionError:
    st.warning(
        "Start FastAPI to display the chart."
    )

except Exception as e:
    st.warning(f"Unable to load chart: {e}")