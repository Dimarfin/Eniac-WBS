import warnings; 
warnings.simplefilter('ignore')
import pandas as pd
import re
import seaborn as sns
import matplotlib.pyplot as plt

#pd.set_option('display.max_rows', 1000)
#pd.set_option("display.max_colwidth", 100)
path='D:\Dima\Study\WBS\Week 03 - database with pandas - Eniac\Code\Project\Data\\'

orders=pd.read_csv(path+'orders_clean.csv')
products=pd.read_csv(path+'products_clean.csv')
orderlines=pd.read_csv(path+'orderlines_clean.csv')
brands = pd.read_csv(path+'brands.csv')


df_list = [orderlines, orders, brands, products]
files = ['orderlines','orders','brands','products']


products["sku_short"] = products.sku.str[0:3]

prod_brands = products.merge(brands, how = "left", left_on = "sku_short", right_on = "short")

prod_brands.drop(columns = ["sku_short", "short"], inplace = True)

prod_brands.rename(columns = {"long": "brand"}, inplace = True)

prod_brands["category"] = ""

def categorize_product(row):
    if row["brand"] == "Apple":
        if re.search(r"watch", row["name"], re.IGNORECASE):
            return "Smartwatch" 
        elif re.search(r"(case|sleeve|skin|cover|protect)", row["name"], re.IGNORECASE):
            return "Protection"
        elif re.search(r"(dock|cable|adapter|chargers|strap)", row["name"], re.IGNORECASE):
            return "Accessories"
        elif re.search(r"(iMac|Mac Mini|Mac Pro)", row["name"], re.IGNORECASE):
            return "Desktop computer"
        elif re.search(r"MacBook", row["name"], re.IGNORECASE):
            return "Laptop computer"
        elif re.search(r"iPhone", row["name"], re.IGNORECASE):
            return "Smartphone"
        elif re.search(r"iPad", row["name"], re.IGNORECASE):
            return "Tablet"
        elif re.search(r"iPod", row["name"], re.IGNORECASE):
            return "Audio"         
        elif re.search(r"(keyboard|mouse|trackpad)", row["name"], re.IGNORECASE):
            return "Keyboard & mouse"
        elif re.search(r"(monitor|display)", row["name"], re.IGNORECASE):
            return "Display"       
        else:
            return "Others"
    else:
        if re.search(r"(keyboard|mouse|keypad|numpad)", row["name"], re.IGNORECASE):
            return "Keyboard & mouse"
        elif re.search(r"(headphones|microphones|speaker|headset)", row["name"], re.IGNORECASE):
            return "Audio"  
        elif re.search(r"(drive|disk|raid|SSD|SSHD|SD|HDD)", row["name"], re.IGNORECASE):
            return "External storage"  
        elif re.search(r"(memory)", row["name"], re.IGNORECASE):
            return "Memory"
        elif re.search(r"(monitor|display)", row["name"], re.IGNORECASE):
            return "Display"  
        elif re.search(r"(case|sleeve|skin|cover|protect)", row["name"], re.IGNORECASE):
            return "Protection"  
        elif re.search(r"repair", row["name"], re.IGNORECASE):
            return "Repair services"
        elif re.search(r"camera", row["name"], re.IGNORECASE):
            return "Camera"
        elif re.search(r"(dock|cable|adapter|chargers|stand|trackpad|battery)", row["name"], re.IGNORECASE):
            return "Accessories"
        elif re.search(r"(hub|switch|router)", row["name"], re.IGNORECASE):
            return "Network"
        else:
            return "Others"

prod_brands["category"] = prod_brands.apply(categorize_product, axis = 1)

olpb = orderlines.merge(prod_brands, how='left', left_on='sku', right_on='sku')

olpbo = olpb.merge(orders, how='left', left_on='id_order', right_on='order_id')

olpbo=olpbo.query("state=='Completed'")

df=pd.DataFrame(olpbo[['sku','product_quantity','unit_price','price']])
df['discount'] = round(100*(df['price']-df['unit_price'])/df['price'])
df1=df.groupby(['sku']).agg({'discount':'mean','product_quantity':'sum','price':'mean'})

fig3, ax31 = plt.subplots(figsize=(9, 5))
sns.scatterplot(data=df1,x='discount',y='product_quantity',hue='price',hue_norm=(0,1000),s=120,alpha=0.5)
plt.xlim(0,100)
plt.ylim(0,1000)