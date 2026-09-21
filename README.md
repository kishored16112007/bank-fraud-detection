# 💳 Credit Card Fraud Detection System

An end-to-end machine learning application for detecting potentially fraudulent credit card transactions using **Python, Scikit-learn, FastAPI, PostgreSQL, and Streamlit**.

The system takes transaction features as input, uses a trained machine learning model to classify the transaction as **Normal** or **Fraud**, calculates a fraud probability, and stores the prediction in PostgreSQL for transaction history.

---

## 🚀 Project Overview

Credit card fraud detection is a challenging machine learning problem because fraudulent transactions are extremely rare compared with legitimate transactions.

This project demonstrates a complete ML application workflow:

```text
Transaction Input
       ↓
Streamlit Dashboard
       ↓
FastAPI REST API
       ↓
Machine Learning Model
       ↓
Fraud / Normal Prediction
       ↓
PostgreSQL Database
       ↓
Transaction History
```

---

## 🎯 Objectives

* Detect potentially fraudulent credit card transactions.
* Handle highly imbalanced transaction data.
* Train and evaluate machine learning models.
* Expose the trained model through a REST API.
* Store prediction results in PostgreSQL.
* Provide an interactive Streamlit dashboard.
* Display recent transaction history and fraud statistics.

---

## 🧠 Machine Learning

### Dataset

The project uses the **Credit Card Fraud Detection** dataset from Kaggle.

Dataset:

`mlg-ulb/creditcardfraud`

The dataset contains:

* **284,807 transactions**
* **31 columns**
* `Time`
* `V1`–`V28`
* `Amount`
* `Class`

The target column is:

```text
Class = 0 → Normal transaction
Class = 1 → Fraudulent transaction
```

The `V1`–`V28` features are anonymized numerical features from the original dataset.

> The original dataset is not included in this GitHub repository because the CSV file is larger than GitHub's standard file-size limit. It is downloaded and stored locally for model development.

---

## 🔄 Machine Learning Pipeline

### 1. Data Loading

The dataset is loaded using Pandas.

### 2. Exploratory Data Analysis

The project analyzes:

* Dataset shape
* Missing values
* Duplicate records
* Class distribution
* Transaction amount distribution
* Feature correlations
* Normal vs fraudulent transactions

### 3. Train-Test Split

The data is divided into:

```text
80% → Training
20% → Testing
```

A stratified split is used to preserve the fraud/normal class distribution.

### 4. Feature Scaling

The `Amount` feature is standardized using `StandardScaler`.

The scaler is fitted only on the training data and then applied to the test data to avoid data leakage.

### 5. Models

The project experiments with:

* Logistic Regression
* Class-Weighted Logistic Regression
* Random Forest

Because fraud detection is highly imbalanced, class-weighted Logistic Regression is used as the lightweight deployment model.

---

## 📊 Model Evaluation

The models are evaluated using metrics that are useful for imbalanced classification:

* Precision
* Recall
* F1-Score
* ROC-AUC
* PR-AUC
* Confusion Matrix

**PR-AUC** is particularly useful for evaluating performance when the positive fraud class is rare.

---

## ⚡ FastAPI

FastAPI provides the REST API for the machine learning model.

### API Endpoints

#### Health Check

```text
GET /
```

Returns:

```json
{
  "message": "Credit Card Fraud Detection API is running"
}
```

#### Fraud Prediction

```text
POST /predict
```

The endpoint receives transaction features and returns:

```json
{
  "prediction": "Normal",
  "fraud_probability": 0.0123
}
```

#### Transaction History

```text
GET /transactions
```

Returns recently stored transaction predictions from PostgreSQL.

FastAPI also provides an interactive API documentation page through Swagger UI:

```text
http://127.0.0.1:8000/docs
```

---

## 🗄️ PostgreSQL

PostgreSQL is used to store prediction results.

### Database

```text
fraud_detection
```

### Table

```text
transactions
```

The table stores:

| Column              | Description                  |
| ------------------- | ---------------------------- |
| `id`                | Unique transaction record ID |
| `transaction_time`  | Transaction time             |
| `amount`            | Transaction amount           |
| `prediction`        | Normal or Fraud              |
| `fraud_probability` | Model probability            |
| `created_at`        | Record creation timestamp    |

---

## 🖥️ Streamlit Dashboard

The Streamlit dashboard provides an interactive interface for the application.

Features include:

* Transaction input
* V1–V28 feature input
* Fraud prediction
* Fraud probability
* Total transaction count
* Fraud transaction count
* Normal transaction count
* Average fraud probability
* Recent transaction history
* Fraud vs Normal transaction chart

---

## 📁 Project Structure

```text
bank-fraud-detection/
│
├── app/
│   ├── main.py
│   ├── database.py
│   └── dashboard.py
│
├── data/
│   ├── raw/
│   │   └── creditcard.csv
│   └── processed/
│
├── models/
│   ├── fraud_detection_model.pkl
│   └── amount_scaler.pkl
│
├── notebooks/
│   └── 01_fraud_detection_eda.ipynb
│
├── src/
│
├── download_dataset.py
├── requirements.txt
├── .gitignore
└── README.md
```

> Dataset files and trained model files are excluded from the GitHub repository where appropriate through `.gitignore`.

---

## 🛠️ Technologies Used

### Programming

* Python

### Machine Learning

* Pandas
* NumPy
* Scikit-learn
* Joblib

### API

* FastAPI
* Uvicorn

### Database

* PostgreSQL
* Psycopg2

### Dashboard

* Streamlit

### Data Visualization

* Matplotlib
* Seaborn

### Development Tools

* Jupyter Notebook
* VS Code
* Git
* GitHub

---

## ⚙️ Installation

Clone the repository:

```bash
git clone https://github.com/kishored16112007/bank-fraud-detection.git
```

Move into the project:

```bash
cd bank-fraud-detection
```

Create a virtual environment:

```bash
python -m venv venv
```

Activate it on Git Bash:

```bash
source venv/Scripts/activate
```

Install dependencies:

```bash
python -m pip install -r requirements.txt
```

---

## 📥 Dataset Setup

The dataset is not stored in the GitHub repository.

Download the Credit Card Fraud Detection dataset and place:

```text
creditcard.csv
```

inside:

```text
data/raw/
```

Alternatively, use the included dataset download script:

```bash
python download_dataset.py
```

---

## 🗄️ PostgreSQL Setup

Create a PostgreSQL database named:

```text
fraud_detection
```

Create the transactions table:

```sql
CREATE TABLE transactions (
    id SERIAL PRIMARY KEY,
    transaction_time DOUBLE PRECISION,
    amount DOUBLE PRECISION NOT NULL,
    prediction VARCHAR(20),
    fraud_probability DOUBLE PRECISION,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

Update the PostgreSQL connection details in:

```text
app/database.py
```

Do not upload database passwords to GitHub.

---

## ▶️ Running the Application

### Start FastAPI

Open Git Bash:

```bash
cd bank-fraud-detection/app
```

Then:

```bash
python -m uvicorn main:app --reload
```

FastAPI will run at:

```text
http://127.0.0.1:8000
```

Swagger documentation:

```text
http://127.0.0.1:8000/docs
```

### Start Streamlit

Open another terminal:

```bash
cd bank-fraud-detection
```

Run:

```bash
python -m streamlit run app/dashboard.py
```

The Streamlit dashboard will open in your browser.

---

## 🔐 Security

Sensitive information such as:

* PostgreSQL passwords
* Environment variables
* Large datasets
* Local virtual environments

should not be committed to GitHub.

The project uses `.gitignore` to exclude local files that should not be uploaded.

---

## 📌 Key Learning Outcomes

Through this project, the following concepts were practiced:

* Machine learning classification
* Imbalanced datasets
* Data preprocessing
* Feature scaling
* Stratified train-test splitting
* Model evaluation
* Precision, Recall and F1-Score
* ROC-AUC and PR-AUC
* REST API development
* FastAPI
* PostgreSQL database integration
* Streamlit application development
* Git and GitHub
* End-to-end ML application development

---

## 👨‍💻 Author

**Kishore D**

B.Tech Applied AI

GitHub:
https://github.com/kishored16112007
