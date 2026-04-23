import pandas as pd
pd.set_option('display.max_columns', None)
pd.set_option('display.max_colwidth', None)
pd.set_option('display.width', 1000)

# 1. DATEN IMPORTIEREN
inventory_data = {
    'p_id': [10, 20, 30, 40, 50],
    'p_name': ['Monitor', 'Keyboard', 'Mouse', 'Laptop', 'HDMI Cable'],
    'purchase_price': [150, 20, 10, 800, 5]
}
df_inventory = pd.DataFrame(inventory_data)

transactions_data = {
    'p_id': [10, 20, 30, 10, 40, 60, 50, 10], # 60 - этого товара нет в инвентаре!
    'sale_price': [250, 45, 25, 240, 1500, 50, 15, 260], # 1500 - явная аномалия (Laptop по ошибке?)
    'quantity': [2, 5, 10, 1, 1, 3, 2, 1],
    'city': ['Berlin', 'Munich', 'Berlin', 'Dortmund', 'Berlin', 'Munich', 'Dortmund', 'Berlin']
}
df_transactions = pd.DataFrame(transactions_data)

# 2. VERARBEITUNG

# Merge / Tabellen zusammenführen
df_final = pd.merge(df_transactions,df_inventory, on ='p_id', how='left')

# Cleaning
df_clean = df_final.dropna(subset=['p_id']).copy()
df_clean = df_clean[df_clean['p_id'] >= 0]
#Outliers
limit = df_clean ['sale_price'].quantile(0.90)
df_final = df_clean[df_clean['sale_price'] <= limit]
#Profit calculation
df_final['profit'] = (df_final['sale_price'] - df_final['purchase_price']) * df_final['quantity']
df_final['revenue'] = df_final['sale_price']*df_final['quantity']
#Aggregation
result = df_final.groupby('city').agg(
    total_profit=('profit','sum'),
    avg_sale_price=('sale_price','mean'),
    unique_product=('p_id','nunique'),
    total_revenue=('revenue', 'sum')
).reset_index()

print("FINALE ANALYSE")
result['margin'] = result['total_profit'] / result['total_revenue'] * 100
result['margin'] = result['margin'].round(2)
print(result)
