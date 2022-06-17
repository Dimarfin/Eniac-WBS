import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

#path='D:\Dima\Study\WBS\Week 03 - database with pandas - Eniac\Data\\'
path = '..\Data\\'

orders=pd.read_csv(path+'orders_clean.csv')
products=pd.read_csv(path+'products_clean.csv')
orderlines=pd.read_csv(path+'orderlines_clean.csv')
brands=pd.read_csv(path+'brands.csv')

months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 
          'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']

orderlines['unit_price_total'] = orderlines['product_quantity'] * orderlines['unit_price']
orders['completed']= (orders['state']=='Completed')

#Preparing data frame for revenue over month plot
#----------------------------------------
#orders_compl=orders.query("state=='Completed'")

olo=(
    orderlines
    .merge(orders, how='left', left_on='id_order', right_on='order_id')
)

olo['date'] = pd.to_datetime(olo['date'])

olo = (olo
            .assign(year = olo['date'].dt.strftime('%Y'), 
                    month = olo['date'].dt.strftime('%b')
    )
)

olo['month'] = pd.Categorical(olo['month'], categories=months, ordered=True)

######################
olo_group_ym = olo.groupby(['year','month']).agg({'unit_price_total':'sum','state':'count','completed':'sum'})

olo_group_ym=olo_group_ym.loc[('2017','Jan'):('2018','Mar'),:]

olo_group_ym.reset_index(inplace=True)
olo_group_ym['unit_price_total_M'] = olo_group_ym['unit_price_total']/1e6

olo_group_ym['conv_rate'] = 100*olo_group_ym['completed']/olo_group_ym['state']

######################
oloc=olo.query("state=='Completed'")

oloc_group_ym = oloc.groupby(['year','month']).agg({'unit_price_total':'sum','state':'count','completed':'sum'})

oloc_group_ym=oloc_group_ym.loc[('2017','Jan'):('2018','Mar'),:]

oloc_group_ym.reset_index(inplace=True)
oloc_group_ym['unit_price_total_M'] = oloc_group_ym['unit_price_total']/1e6

oloc_group_ym['conv_rate'] = 100*oloc_group_ym['completed']/oloc_group_ym['state']


#Preparing data frame for the average discount (in %) over month plot
#-------------------------------------------------------------------
orderlines['date'] = pd.to_datetime(orderlines['date'])
olp = orderlines.merge(products, how='left', left_on='sku', right_on='sku')

olpo = olp.merge(orders, how='left', left_on='id_order', right_on='order_id')


olpo = (
olpo
    .assign(year = olpo['date'].dt.strftime('%Y'), 
           month = olpo['date'].dt.strftime('%b')
    )
)

olpo['month'] = pd.Categorical(olpo['month'], categories=months, ordered=True)

olpoc=olpo.copy()#olpo.query("state=='Completed'")
#olpoc=olpo.query("state=='Completed'")

olpoc_group_ym = olpoc.groupby(['year','month']).agg({'unit_price':'sum','price':'sum'})

olpoc_group_ym=olpoc_group_ym.loc[('2017','Jan'):('2018','Mar'),:]

olpoc_group_ym['discount'] = round(100*(olpoc_group_ym['price']-olpoc_group_ym['unit_price'])/olpoc_group_ym['price'])

olpoc_group_ym.reset_index(inplace=True)

#Ploting
################
rev_color='red'
conv_color='green'
disc_color='blue'
legend_fs='20'

#Conversion rate vs discounts
fig1, ax11 = plt.subplots(figsize=(18, 10))
sns.lineplot(data=olo_group_ym,x='month',y='conv_rate',style='year',ax=ax11,marker="o",color=conv_color, markersize=8)
plt.ylabel('Conversion rate, %',fontsize=26)
plt.xlabel('Month',fontsize=26)
ax11.yaxis.label.set_color(conv_color)
ax11.spines['left'].set_color(conv_color)
ax11.tick_params(axis='y', colors=conv_color,labelsize=18)
ax11.tick_params(axis='both', which='major', labelsize=18)
plt.legend(fontsize=legend_fs, title_fontsize='40')

ax12 = ax11.twinx()
sns.lineplot(data=olpoc_group_ym,x='month',y='discount',style='year',ax=ax12,marker="o",color=disc_color, markersize=8)
plt.ylabel('Average discount, %',fontsize=26)
ax12.yaxis.label.set_color(disc_color)
ax12.spines['right'].set_color(disc_color)
ax12.spines['left'].set_color(conv_color)
ax12.tick_params(axis='y', colors=disc_color,labelsize=18)
plt.legend(fontsize=legend_fs, title_fontsize='40')
#ax12.tick_params(axis='x', labelsize=18)

#Revenue vs discounts
fig2, ax21 = plt.subplots(figsize=(18, 10))
sns.lineplot(data=oloc_group_ym,x='month',y='unit_price_total_M',style='year',ax=ax21,marker="o",color=rev_color, markersize=8)
plt.ylabel('Revenue, M euro',fontsize=26)
plt.xlabel('Month',fontsize=26)
ax21.yaxis.label.set_color(rev_color)
ax21.spines['left'].set_color(rev_color)
ax21.tick_params(axis='y', colors=rev_color,labelsize=18)
ax21.tick_params(axis='both', which='major', labelsize=18)
plt.legend(fontsize=legend_fs, title_fontsize='40')


ax22 = ax21.twinx()
sns.lineplot(data=olpoc_group_ym,x='month',y='discount',style='year',ax=ax22,marker="o",color=disc_color, markersize=8)
plt.ylabel('Average discount, %',fontsize=26)
ax22.yaxis.label.set_color(disc_color)
ax22.spines['right'].set_color(disc_color)
ax22.spines['left'].set_color(rev_color)
ax22.tick_params(axis='y', colors=disc_color,labelsize=18)
plt.legend(fontsize=legend_fs, title_fontsize='40')
#ax22.tick_params(axis='x', labelsize=18)


##############################
df=pd.DataFrame(olpoc_group_ym[['month','discount']])
df['rev']=olo_group_ym['unit_price_total_M']
df['conv_rate']=olo_group_ym['conv_rate']

fig3, ax31 = plt.subplots(figsize=(9, 5))
sns.scatterplot(data=df,x='discount',y='conv_rate',hue='month',s=120)

#fitting a line
x=np.array(df.discount)
y=np.array(df.conv_rate)
coef = np.polyfit(x,y,1)
poly1d_fn = np.poly1d(coef)

x1=np.arange(0,20,1)
plt.plot(x1, poly1d_fn(x1), '--g')

#plt.ylim(0,3)
#plt.xlim(4,16)
plt.xlabel('Average monthly discount, %',fontsize=18)
plt.ylabel('Conversion rate,%',fontsize=18)
ax31.tick_params(axis='y',labelsize=14)

######################################
df=pd.DataFrame(olpoc_group_ym[['month','discount']])
df['rev']=oloc_group_ym['unit_price_total_M']
df['conv_rate']=oloc_group_ym['conv_rate']

fig4, ax41 = plt.subplots(figsize=(9, 5))
sns.scatterplot(data=df,x='discount',y='rev',hue='month',s=120)

#fitting a line
x=np.array(df.discount)
y=np.array(df.rev)
coef = np.polyfit(x,y,1)
poly1d_fn = np.poly1d(coef)

x1=np.arange(0,20,1)
plt.plot(x1, poly1d_fn(x1), '--r')

#plt.ylim(0,3)
#plt.xlim(4,16)
plt.xlabel('Average monthly discount, %',fontsize=18)
plt.ylabel('Monthly revenue, M euro',fontsize=18)
ax41.tick_params(axis='y',labelsize=14)
