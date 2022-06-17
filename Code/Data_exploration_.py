import pandas as pd
path = '..\Data\\'

orders=pd.read_csv(path+'orders.csv')
products=pd.read_csv(path+'products.csv')
orderlines=pd.read_csv(path+'orderlines.csv')
brands=pd.read_csv(path+'brands.csv')

#General info
##############
print('orders.csv :')
print(orders.info())
print('\n')

print('products.csv :')
print(products.info())
print('\n')

print('orderlines.csv :')
print(orderlines.info())
print('\n')

print('brands.csv :')
print(brands.info())
print('\n')

#Data overveiw
################
print('orders.csv :')
print(orders.sample(5))
print('\n')

print('products.csv :')
print(products.sample(5))
print('\n')

print('orderlines.csv :')
print(orderlines.sample(5))
print('\n')

print('brands.csv :')
print(brands.sample(5))
print('\n')

#Check Nans
###########
print('Nan in orders:')
print(orders.isna().sum())
print(' ')

print('Nan in orderlines:')
print(orderlines.isna().sum())
print(' ')

print('Nan in products:')
print(products.isna().sum())
print(' ')

print('Nan in brands:')
print(brands.isna().sum())
print(' ')

#Check duplicates
#################
print('Duplicates in orders: ',orders.duplicated().sum(),'\n ')
print('Duplicates in orderliness: ',orderlines.duplicated().sum(),'\n ')
print('Duplicates in products: ',products.duplicated().sum(),'\n ')
print('Duplicates in brands: ',brands.duplicated().sum(),'\n ')
