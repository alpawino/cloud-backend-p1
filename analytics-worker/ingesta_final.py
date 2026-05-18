import pandas as pd
from sqlalchemy import create_engine
import boto3
from pymongo import MongoClient
import os

# 1. Configuración de conexiones usando la IP PRIVADA
# IP de la base de datos de Jean: 172.31.82.16
mysql_engine = create_engine('mysql+pymysql://root:root@172.31.82.16:3306/usersdb')
postgres_engine = create_engine('postgresql+psycopg2://root:root@172.31.82.16:5432/orders_db')
mongo_client = MongoClient('mongodb://172.31.82.16:27017/')

# 2. Extracción de datos
print("Extrayendo datos de los 3 microservicios...")

# SQL
df_users = pd.read_sql('SELECT * FROM users', mysql_engine)
df_orders = pd.read_sql('SELECT * FROM orders', postgres_engine)

# MongoDB (Productos)
db = mongo_client['productsDB']
collection = db['products']
df_products = pd.DataFrame(list(collection.find()))
# Eliminamos el campo _id de Mongo para que el CSV sea limpio
if '_id' in df_products.columns:
    df_products = df_products.drop(columns=['_id'])

# 3. Guardar localmente
df_users.to_csv('users_final.csv', index=False)
df_orders.to_csv('orders_final.csv', index=False)
df_products.to_csv('products_final.csv', index=False)

# 4. Carga a tu nuevo bucket S3
bucket_name = os.environ.get('S3_BUCKET', 'ingesta-proyecto-final-2026')
s3 = boto3.client('s3')

print(f"Subiendo archivos al bucket {bucket_name}...")
s3.upload_file('users_final.csv', bucket_name, 'ingesta/users_final.csv')
s3.upload_file('orders_final.csv', bucket_name, 'ingesta/orders_final.csv')
s3.upload_file('products_final.csv', bucket_name, 'ingesta/products_final.csv')

print("¡Ingesta completa! Los 3 microservicios están en S3.")
