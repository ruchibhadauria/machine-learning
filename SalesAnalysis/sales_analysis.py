# Sales Analysis

## Import Necessary Libraries
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

## Loading the data
sales_jan = pd.read_csv('/content/Sales_January_2019.csv')
sales_feb = pd.read_csv('/content/Sales_February_2019.csv')
sales_mar = pd.read_csv('/content/Sales_March_2019.csv')
sales_apr = pd.read_csv('/content/Sales_April_2019.csv')
sales_may = pd.read_csv('/content/Sales_May_2019.csv')
sales_jun = pd.read_csv('/content/Sales_June_2019.csv')
sales_jul = pd.read_csv('/content/Sales_July_2019.csv')
sales_aug = pd.read_csv('/content/Sales_August_2019.csv')
sales_sep = pd.read_csv('/content/Sales_September_2019.csv')
sales_oct = pd.read_csv('/content/Sales_October_2019.csv')
sales_nov = pd.read_csv('/content/Sales_November_2019.csv')
sales_dec = pd.read_csv('/content/Sales_December_2019.csv')

### Merging all months of sales data into a single file
sales = pd.concat([sales_jan, sales_feb, sales_mar, sales_apr, sales_may, sales_jun, sales_jul, sales_aug, sales_sep,
                   sales_oct, sales_nov, sales_dec], ignore_index=True, axis=0)
sales

#### Dropping all the null values
sales.dropna(how='all', inplace=True)

#### Creating a month column
sales['Month'] = sales['Order Date'].apply(lambda x: str(x).split('/')[0])

#### Deleting rows with Order Date as Month value
sales.drop(sales[sales['Month']=='Order Date'].index, inplace=True)
sales.info()

#### Changing datatype of columns
sales['Month'] = sales['Month'].astype('int32')
sales['Quantity Ordered'] = sales['Quantity Ordered'].astype('int32')
sales['Price Each'] = sales['Price Each'].astype('float32')

#### Creating a sale column
sales['Sale'] = sales['Quantity Ordered'] * sales['Price Each']
sales

#### What is the best month for sales? How much was earned that month?
grouped_by_month = pd.DataFrame(sales.groupby(by='Month').sum())
grouped_by_month

plt.figure(figsize=(15, 5))
ax = sns.barplot(x=grouped_by_month.index, y=grouped_by_month['Sale'], data=grouped_by_month);
for p in ax.patches:
    ax.annotate('{:.0f}'.format(p.get_height()), (p.get_x()+0.15, p.get_height()+1))

Month of december has highest sales of around 46 lacs.

#### What city had the highest number of sales?
def city_state(x):
    city = x.split(',')[1]
    state = x.split(',')[2].split(' ')[1]
    return city + '(' + state + ')'

sales['City'] = sales['Purchase Address'].apply(lambda x: city_state(x))
sales.head()

grouped_by_city = pd.DataFrame(sales.groupby(by='City').sum())
grouped_by_city

plt.figure(figsize=(18, 4))
a = sns.barplot(x=grouped_by_city.index, y=grouped_by_city['Sale'], data=grouped_by_city)
for p in a.patches:
    a.annotate('{:.0f}'.format(p.get_height()), (p.get_x()+0.15, p.get_height()+1))

#### What time should we display advertisements to maximize likelihood of customer's buying product?
sales['Order Date'] = pd.to_datetime(sales['Order Date'])
sales['Hour'] = sales['Order Date'].apply(lambda x: x.hour)
sales.head()

grouped_by_hour = pd.DataFrame(sales.groupby(by='Hour').count())
grouped_by_hour

plt.figure(figsize=(24, 4))
a = sns.barplot(x=grouped_by_hour.index, y=grouped_by_hour['Sale'], data=grouped_by_hour)
for p in a.patches:
    a.annotate('{:.0f}'.format(p.get_height()), (p.get_x()+0.15, p.get_height()+1))

#### What products are most often sold together?
grouped_by_order_id = sales.groupby('Order ID')['Order ID', 'Product'].transform(lambda x: ','.join(x))

grouped_by_order_id

from itertools import combinations
from collections import Counter

count = Counter()

for row in grouped_by_order_id['Product']:
    row_list = row.split(',')
    count.update(Counter(combinations(row_list, 2)))

for key, value in count.most_common(9):
    print(key, value)

#### What product sold the most? Why do you think it sold the most?
grouped_by_product = sales.groupby('Product').sum()
grouped_by_product

plt.figure(figsize=(24, 4))
a = sns.barplot(x=grouped_by_product.index, y=grouped_by_product['Quantity Ordered'], data=grouped_by_product)

for p in a.patches:
    a.annotate('{:.0f}'.format(p.get_height()), (p.get_x()+0.15, p.get_height()+1))

plt.xticks(rotation=90)
plt.show()

price = sales.groupby('Product').mean()['Price Each']
print(price)

plt.bar(grouped_by_product.index, grouped_by_product['Quantity Ordered'])
plt.xticks(rotation = 90)
plt.bar(price.index, price)

fig, ax = plt.subplots()
ax2 = ax.twinx()

ax.bar(grouped_by_product.index, grouped_by_product['Quantity Ordered'])
ax2.plot(price.index, price, color='r')

ax.set_ylabel('Quantity Ordered', color='b')
ax.set_xlabel('Product')
ax2.set_ylabel('Price', color='r')
ax.set_xticklabels(labels=price.index, rotation=90)

plt.show()

