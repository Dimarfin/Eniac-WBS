import pandas as pd
path = '..\Data\\'

orders=pd.read_csv(path+'orders.csv')
products=pd.read_csv(path+'products.csv')
orderlines=pd.read_csv(path+'orderlines.csv')
brands=pd.read_csv(path+'brands.csv')

#1
#------------------------------------

#Remove rows with Nans
orders.dropna(inplace=True)
products = products[products['price'].notna()]
products.reset_index()

#Remove rows with duplicates
products.drop_duplicates(inplace=True)

#Fixing products prices
#######################
products['dots'] = products['price'].str.count('\.')
#Dealing with 1 or 0 dots - drop products with price with two or more dots
p_temp=products.query('dots <= 1')
p_temp['price'] = pd.to_numeric(p_temp['price']).round(2)
p_temp.drop(['dots'], axis=1, inplace=True)

products = p_temp
products.reset_index()

#Change date datatype
#####################
orders['created_date'] = pd.to_datetime(orders['created_date'])
orderlines['date'] = pd.to_datetime(orderlines['date'])

#Remove not connected items
###########################

#Take only orderlines with 'sku' presented in products
orderlines = (orderlines
          .assign(check_sku = orderlines['sku'].isin(products['sku']))
          .query("check_sku==True")
         )
orderlines.drop('check_sku', axis='columns',inplace=True)

#Take only orderlines which are presented in orders
orderlines = (orderlines
              .assign(check_orders = orderlines['id_order'].isin(orders['order_id']))
              .query("check_orders==True")
              )
orderlines.drop('check_orders', axis='columns',inplace=True)

#Take only ordres which contane items in orderlines
orders = (orders
          .assign(check_orders = orders['order_id'].isin(orderlines['id_order']))
          .query("check_orders==True")
         )
orders.drop('check_orders', axis='columns',inplace=True)

#2
#------------------------------------

#Removing extra dots from unit_price and converting to numeric
orderlines = orderlines.assign(unit_price_nd = orderlines['unit_price'].str.replace('\.','', regex=True))
orderlines['decimals'] = orderlines['unit_price_nd'].str[-2:]
orderlines['integers'] = orderlines['unit_price_nd'].str[:-2]
orderlines['new_unit_price'] = orderlines['integers'] + '.' + orderlines['decimals']
orderlines['unit_price'] = pd.to_numeric(orderlines['new_unit_price'])
# drop 'auxiliary' columns
orderlines.drop(['unit_price_nd','decimals','integers','new_unit_price'], axis=1, inplace=True)

# create a new column "unit_price_total" by multiplying product_quantity times unit_price
orderlines['unit_price_total'] = orderlines['product_quantity'] * orderlines['unit_price']
#
print("Difference between sum of sold items prices and totaty paid amount")
print(orderlines['unit_price_total'].sum() - orders['total_paid'].sum())

#merge orderlines and orders to solve price mismatch problem
orders_info = (
orderlines
    .groupby('id_order')
    .agg({'unit_price_total':'sum'})
    .merge(orders, how='left', left_on='id_order', right_on='order_id')
    .copy()
)
orders_info['price_difference'] = orders_info['unit_price_total'] - orders_info['total_paid']
print("Info about difference between sum of sold items prices and totaty paid amount")
print(orders_info['price_difference'].describe())
#there are outliers in price differens -> some rows of the table are corrupted

#remove outliers
orders_info_new = (
orders_info[abs(orders_info['price_difference'])
            <abs(10*orders_info['price_difference'].mean())
            ].copy()
)

print("Info about difference between sum of sold items prices and totaty paid amount")
print("after removing outliers")
print(orders_info_new['price_difference'].describe())

orders = orders[orders['order_id'].isin(orders_info_new['order_id'])]
######orders.drop('check_orders', axis='columns',inplace=True)

orderlines = orderlines[orderlines['id_order'].isin(orders_info_new['order_id'])]
######orderlines.drop('check_orders', axis='columns',inplace=True)

products = products[products['sku'].isin(orderlines['sku'])]

orderlines.to_csv(path+'orderlines_clean.csv', index=False)
orders.to_csv(path+'orders_clean.csv', index=False)
products.to_csv(path+'products_clean.csv', index=False) 