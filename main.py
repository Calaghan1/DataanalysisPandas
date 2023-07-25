import pandas as pd
import numpy as np

df = pd.read_json('trial_task.json')
def first(df):
    column_data = df['warehouse_name'].unique()
    result = []
    for c in column_data:
        tarif_for_whirehous = {}
        sum_of_quantity = 0
        filtered_data = df[df['warehouse_name'] == c].head(1)
        highway_cost = filtered_data['highway_cost'].tolist()[0]
        filtered_data = filtered_data['products'].tolist()[0]
        # print(filtered_data)
        for f in filtered_data:
            sum_of_quantity += f['quantity']
            # sum_of_quantity += 1
        
        tarif_for_whirehous[c] = highway_cost/sum_of_quantity * -1
        result.append(tarif_for_whirehous)
    # print(column_data)
    data = []
    for r in result:
        for a in r:
            data.append([a, r[a]])
    d = pd.DataFrame(data, columns= ['warehouse_name', 'tarif'])
    return(result)
    
def second(df):
    buf_dic ={}
    tarif = first(df)
    for index, row in df.iterrows():
        
        for t in tarif:
            if t.get(row['warehouse_name']):
                cost = t[row['warehouse_name']]
        for product in row['products']:
            # print(product)
            # print(buf_dic.get(product['product']))
            if not buf_dic.get(product['product']):
                buf_dic[product['product']] = {}
                buf_dic[product['product']]['quantity'] = 0
                buf_dic[product['product']]['income'] = 0
                buf_dic[product['product']]['expenses'] = 0
                buf_dic[product['product']]['profit'] = 0
            buf_dic[product['product']]['quantity'] += product['quantity'] 
            buf_dic[product['product']]['expenses'] += product['quantity'] * cost
            buf_dic[product['product']]['income'] = product['price'] * buf_dic[product['product']]['quantity']
            buf_dic[product['product']]['profit'] = buf_dic[product['product']]['income'] - buf_dic[product['product']]['expenses']
    data = []
    # print(buf_dic)
    for a in buf_dic:
        data.append([a, buf_dic[a]['quantity'], buf_dic[a]['income'], buf_dic[a]['expenses'],
                     buf_dic[a]['profit']])
    d = pd.DataFrame(data, columns= ['product', 'quantity', 'income', 'expenses', 'profit'])
    return(d, buf_dic)      
    

def third(df):
    
    buf_dic = {}
    i = 0
    tarif = first(df)
    medium_order_profit = 0
    for index, row in df.iterrows():
        # print(row)
        order_profit = 0
        for t in tarif:
            if t.get(row['warehouse_name']):
                cost = t[row['warehouse_name']]
        for product in row['products']:
            order_profit += product['price'] * product['quantity'] - product['quantity'] * cost
        buf_dic[row['order_id']] = order_profit
        medium_order_profit += order_profit
        i += 1
    data = []
    for a in buf_dic:
        data.append([a, buf_dic[a]])
    d  = pd.DataFrame(data, columns=['order_id', 'order_profit'])
    # print(d)
    # print(medium_order_profit/i)
    return(d)
    
def fourth(df):
    buf_dic = {}
    tarif = first(df)
    column_data = df['warehouse_name'].unique()
    for column in column_data:
        orders_of_warehouse = df[df['warehouse_name'] == column]
        # print(orders_of_warehouse)
        ordrers = orders_of_warehouse['products'].tolist()
        # print(products)
        for t in tarif:
            if t.get(column):
                # print(t)
                cost = t[column]
        buf_dic[column] = {}
        buf_dic[column]['prof'] = 0
        for products in ordrers:
            for product in products:
                if not buf_dic[column].get(product['product']):   
                    buf_dic[column][product['product']] = [0,0]
                buf_dic[column][product['product']][0] += product['quantity']
                buf_dic[column][product['product']][1] = (product['price'] * buf_dic[column][product['product']][0])
                # print(column, product['product'],  buf_dic[column][product['product']][1])
                buf_dic[column]['prof'] += (product['price'] * product['quantity'])
                # print(column, product['product'],   buf_dic[column]['prof'], product['price'] * product['quantity'])
    # print(buf_dic)
    table_of_priducts_profit = second(df)[1]
    # print(table_of_priducts_profit)
    tarifs = first(df)
    # print(tarifs)
    data = []
    for a in buf_dic:
        single_data = []
        for tarif in tarifs:
            if tarif.get(a):
                t = tarif[a]
        for key in buf_dic[a].items():
            if key[0] == 'prof':
                sd = key[1]
            else:
                single_data.append(a)
                single_data.append(key[0])
                single_data.append(key[1][0])
                single_data.append(key[1][1])
                single_data.append((key[1][1] - key[1][0] * t)/sd * 100)
                data.append(single_data)
                single_data = []
    d  = pd.DataFrame(data, columns=['warehouse_name', 'product', 'quantity', 'profit', 'percent_profit_product_of_warehouse'])
    return(d)     
                
def fifth(df):
    result = []
    f = fourth(df)
    f = f.sort_values(by='percent_profit_product_of_warehouse', ascending=False)
    column_data = df['warehouse_name'].unique()
    for column in column_data:
        ff = f[f['warehouse_name'] == column]
        # print(ff)
        buf_dic = ff['percent_profit_product_of_warehouse'].tolist()
        for i in range(len(buf_dic) - 1):
            buf_dic[i + 1] += buf_dic[i] 
        result += buf_dic
    
    f['accumulated_percent_profit_product_of_warehouse'] = result
    return f

def sixth(df):
    f = fifth(df)
    buf_dic = f['accumulated_percent_profit_product_of_warehouse'].to_list()
    result = []
    for a in buf_dic:
        if a <= 70:
            result.append('A')
        elif a > 70 and a <= 90:
            result.append('B')
        else:
            result.append('C')
    f['category'] = result    
    return f

if __name__=="__main__":
    print(first(df))
    print(second(df)[0])
    print(third(df))
    print(fourth(df))
    print(fifth(df))
    print(sixth(df))
