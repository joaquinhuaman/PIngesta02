import pandas as pd
import psycopg2
import boto3.session
import boto3
import os
from dotenv import load_dotenv

# --- Cargar variables de entorno ---
load_dotenv()

# --- Datos de conexión a PostgreSQL ---
host = os.getenv("PG_HOST")
port = int(os.getenv("PG_PORT"))
user = os.getenv("PG_USER")
password = os.getenv("PG_PASSWORD")
database = os.getenv("PG_DB")

# --- Datos para S3 ---
s3_bucket = os.getenv("S3_BUCKET")
s3_file_key = os.getenv("S3_KEY", "usuarios.csv")

# --- Conexión PostgreSQL e ingesta ---
conn = psycopg2.connect(
    host=host,
    port=port,
    user=user,
    password=password,
    dbname=database
)

query = "SELECT * FROM usuarios"
df = pd.read_sql(query, conn)
conn.close()

# --- Guardar como CSV ---
file_path = "usuarios.csv"
df.to_csv(file_path, index=False)

# --- Subir a S3 con sesión explícita ---
session = boto3.session.Session(
    aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
    aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
    aws_session_token=os.getenv("AWS_SESSION_TOKEN")
)

s3 = session.client("s3")
s3.upload_file(file_path, s3_bucket, s3_file_key)

print("✅ Ingesta completada: datos PostgreSQL → CSV → S3")