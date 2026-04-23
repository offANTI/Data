import pandas as pd

# 1. Твои исходные данные
customers = pd.DataFrame({
    'customer_id': [101, 102, 103, 104],
    'name': ['Ivan', 'Maria', 'Alex', 'Petr'],
    'city': ['Berlin', 'Munich', 'Berlin', 'Dortmund']
})

orders = pd.DataFrame({
    'order_id': [1, 2, 3, 4, 5],
    'customer_id': [101, 101, 102, 105, 106],
    'amount': [250, 150, 450, 100, 300]
})

# 2. Правильное слияние (Left Join)
# Мы берем ВСЕ заказы и подтягиваем к ним города из таблицы customers
df_merged = pd.merge(orders, customers, on='customer_id', how='left')

# 3. Группировка по городам
# Теперь, когда город и сумма в одной таблице, считаем KPI
city_report = df_merged.groupby("city").agg(
    total_revenue=("amount", "sum"),
    orders_count=("order_id", "count")
).reset_index()

print("--- Отчет по городам ---")
print(city_report)

# 4. Проверка "потеряшек"
# Давай посмотрим на заказы, у которых нет города (где город NaN)
anon_orders = df_merged[df_merged['city'].isna()]
print("\n--- Заказы без города (анонимы) ---")
print(anon_orders)