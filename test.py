import pandas as pd

# Предоставленный пример данных
data = {
    "order_id": 85787,
    "warehouse_name": "хутор близ Диканьки",
    "highway_cost": -90,
    "products": [
        {
            "product": "зеленая пластинка",
            "price": 10,
            "quantity": 3
        },
        {
            "product": "зеленая пластинка",
            "price": 10,
            "quantity": 2
        },
        {
            "product": "билет в Израиль",
            "price": 1000,
            "quantity": 1
        }
    ]
}

# Задача 1: Найти тариф стоимости доставки для каждого склада
tariff_data = [{'warehouse_name': data['warehouse_name'], 'highway_cost_per_product': data['highway_cost']}]

# Задача 2: Найти суммарное количество, суммарный доход, суммарный расход и суммарную прибыль для каждого товара
product_data = []
total_income = 0
total_expenses = 0
for product_info in data['products']:
    product_total_income = product_info['price'] * product_info['quantity']
    product_total_expenses = data['highway_cost'] * product_info['quantity']
    product_profit = product_total_income - product_total_expenses
    total_income += product_total_income
    total_expenses += product_total_expenses
    product_data.append({
        'product': product_info['product'],
        'quantity': product_info['quantity'],
        'income': product_total_income,
        'expenses': product_total_expenses,
        'profit': product_profit
    })

# Задача 3: Составить табличку с id заказа и прибылью полученной с заказа, а также вывести среднюю прибыль заказов
order_profit_data = {'order_id': data['order_id'], 'order_profit': total_income - total_expenses}
average_order_profit = order_profit_data['order_profit']

# Задача 4: Составить табличку 'warehouse_name', 'product', 'quantity', 'profit', 'percent_profit_product_of_warehouse'
warehouse_product_data = []
warehouse_total_profit = 0
for product_info in data['products']:
    product_total_income = product_info['price'] * product_info['quantity']
    print(product_total_income)
    product_total_expenses = data['highway_cost'] * product_info['quantity']
    product_profit = product_total_income - product_total_expenses
    warehouse_total_profit += product_profit
    percent_profit_product_of_warehouse = (product_profit / warehouse_total_profit) * 100
    warehouse_product_data.append({
        'warehouse_name': data['warehouse_name'],
        'product': product_info['product'],
        'quantity': product_info['quantity'],
        'profit': product_profit,
        'percent_profit_product_of_warehouse': percent_profit_product_of_warehouse
    })

# Задача 5: Отсортировать 'percent_profit_product_of_warehouse' по убыванию и рассчитать накопленный процент
warehouse_product_df = pd.DataFrame(warehouse_product_data)
sorted_df = warehouse_product_df.sort_values(by='percent_profit_product_of_warehouse', ascending=False)
sorted_df['accumulated_percent_profit_product_of_warehouse'] = sorted_df['percent_profit_product_of_warehouse'].cumsum()

# Задача 6: Присвоить категории на основе значения накопленного процента
def set_category(accumulated_percent):
    if accumulated_percent <= 70:
        return 'A'
    elif 70 < accumulated_percent <= 90:
        return 'B'
    else:
        return 'C'

sorted_df['category'] = sorted_df['accumulated_percent_profit_product_of_warehouse'].apply(set_category)

# Вывод результатов
print("Задача 1: Тариф стоимости доставки для каждого склада")
print(pd.DataFrame(tariff_data))

print("\nЗадача 2: Суммарное количество, суммарный доход, суммарный расход и суммарная прибыль для каждого товара")
print(pd.DataFrame(product_data))

print("\nЗадача 3: Табличка с id заказа и прибылью полученной с заказа, а также средняя прибыль заказов")
print(pd.DataFrame([order_profit_data]))
print("Средняя прибыль заказов:", average_order_profit)

print("\nЗадача 4: Табличка 'warehouse_name', 'product', 'quantity', 'profit', 'percent_profit_product_of_warehouse'")
print(warehouse_product_df)

print("\nЗадача 5: Табличка с отсортированным 'percent_profit_product_of_warehouse' и накопленным процентом")
print(sorted_df)

print("\nЗадача 6: Табличка с категориями")
print(sorted_df[['warehouse_name', 'product', 'accumulated_percent_profit_product_of_warehouse', 'category']])
