import psycopg2

conn = psycopg2.connect(
    host="localhost",
    database="testdb",
    user="postgres",
    password=123456789
)

cursor = conn.cursor()
def get_orders(customer_id):
    query = """
        SELECT *
        FROM big_orders
        WHERE customer_id = %s
    """

    cursor.execute(query, (customer_id,))
    return cursor.fetchall()


orders = get_orders(100)

print(orders)