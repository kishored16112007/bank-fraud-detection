import psycopg2


def get_connection():
    connection = psycopg2.connect(
        host="localhost",
        port="5432",
        database="fraud_detection",
        user="postgres",
        password="Kishore@1516"
    )

    return connection