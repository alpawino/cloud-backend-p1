import psycopg2
from faker import Faker
import random
from datetime import datetime

fake = Faker()

# Conexión a la base de datos de Órdenes
# Reemplaza <TU_VM_BDS_IP> con la IP privada de tu Máquina 3
try:
    conn = psycopg2.connect(
        dbname="orders_db",
        user="root",
        password="root",
        host="<TU_VM_BDS_IP>",
        port="5432"
    )
    cursor = conn.cursor()
    print("✅ Conectado a PostgreSQL en la VM 3")
except Exception as e:
    print(f"❌ Error conectando a PostgreSQL: {e}")
    exit(1)

# Crear tablas si no existen (por si Hibernate no las ha creado aún)
cursor.execute("""
CREATE TABLE IF NOT EXISTS orders (
    id SERIAL PRIMARY KEY,
    user_id BIGINT NOT NULL,
    status VARCHAR(20) NOT NULL,
    total NUMERIC(12,2) NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE NOT NULL
);

CREATE TABLE IF NOT EXISTS order_details (
    id SERIAL PRIMARY KEY,
    order_id BIGINT NOT NULL REFERENCES orders(id),
    product_id BIGINT NOT NULL,
    quantity INTEGER NOT NULL,
    unit_price NUMERIC(12,2) NOT NULL,
    line_total NUMERIC(12,2) NOT NULL
);
""")
conn.commit()

# Limpiar datos previos
cursor.execute("TRUNCATE TABLE order_details CASCADE;")
cursor.execute("TRUNCATE TABLE orders CASCADE;")
conn.commit()
print("🧹 Tablas limpiadas")

# Generar 20,000 órdenes
print("🚀 Iniciando siembra de 20,000 órdenes...")
statuses = ['CREATED', 'PROCESSING', 'SHIPPED', 'DELIVERED']

try:
    for i in range(20000):
        # 1. Generar la Orden
        user_id = random.randint(1, 20000) # Asume que hay hasta 20k usuarios
        status = random.choice(statuses)
        total = 0
        created_at = fake.date_time_between(start_date='-1y', end_date='now')
        
        cursor.execute(
            "INSERT INTO orders (user_id, status, total, created_at) VALUES (%s, %s, %s, %s) RETURNING id;",
            (user_id, status, total, created_at)
        )
        order_id = cursor.fetchone()[0]
        
        # 2. Generar Detalles para esta orden (1 a 3 productos por orden)
        num_items = random.randint(1, 3)
        order_total = 0
        
        for _ in range(num_items):
            product_id = random.randint(1, 20000) # Asume que hay hasta 20k productos
            quantity = random.randint(1, 5)
            unit_price = round(random.uniform(10.0, 500.0), 2)
            line_total = quantity * unit_price
            order_total += line_total
            
            cursor.execute(
                "INSERT INTO order_details (order_id, product_id, quantity, unit_price, line_total) VALUES (%s, %s, %s, %s, %s);",
                (order_id, product_id, quantity, unit_price, line_total)
            )
            
        # 3. Actualizar el total de la orden
        cursor.execute("UPDATE orders SET total = %s WHERE id = %s;", (order_total, order_id))
        
        # Guardar lotes de 1000
        if (i + 1) % 1000 == 0:
            conn.commit()
            print(f"✅ Insertadas {i + 1} / 20000 órdenes")

    conn.commit()
    print("🎉 ¡20,000 órdenes insertadas con éxito!")

except Exception as e:
    conn.rollback()
    print(f"❌ Error insertando datos: {e}")
finally:
    cursor.close()
    conn.close()
    print("🔌 Conexión cerrada")
