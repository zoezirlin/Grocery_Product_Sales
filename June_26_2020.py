#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jun 24 17:20:58 2020

@author: zoezirlin
"""





# =============================================================================
### Importing libraries ###
import numpy as np
import pandas as pd
import seaborn as sns
from matplotlib import pyplot as plt
from scipy.stats import stats
import statsmodels.api as sm



# =============================================================================
### Importing and reading data basics ###



transaction = pd.read_excel('/Users/zoezirlin/Desktop/Book2.xlsx')
transaction[:10]

# VARIABLE NAMES IN TRANSACTION SET, transactions for 57 products
# Each observation is a difference store and product code and week 
# 3	BASE_PRICE- 	base price of item
# 7	DISPLAY- product was a part of in-store promotional display
# 8	FEATURE- product was in in-store circular
# 9	HHS- number of purchasing houeholds
# 12 PRICE- actual amount charged for the product at shelf
# 13 WEEK_END_DATE- week ending date
# 16 SPEND- total spend (ie- $ sales)
# 19 TPR_ONLY- temporary price reduction only (not advertised as low price)
# 20 UNITS- units sold
# 22 VISITS- number of unique purchases (basekts) that included the product
# 21 UPC- universal product code
# 17 STORE_NUM- store #



store = pd.read_excel('/Users/zoezirlin/Desktop/Book3.xlsx')
store[:10]

# VARIABLE NAMES IN STORE SET
# 0	ADDRESS_CITY_NAME- city
# 1	ADDRESS_STATE_PROV_CODE- state
# 2	AVG_WEEKLY_BASKETS- avg weekly baskets sold in store
# 10 MSA_CODE- metropolitan statistical area
# 11 PARKING_SPACE_QTY- number of parking spaces in store parking lot
# 14	 SALES_AREA_SIZE_NUM- square footage of store
# 15 STORE_APPEAL- retailer's designated store appeal
# 17 STORE_NUM- store #



#Product data includes-
product = pd.read_excel('/Users/zoezirlin/Desktop/Book4.xlsx')
product[:10]

# VARIABLE NAMES IN PRODUCT SET
# 21 UPC- universal product code
# 4	MANUFACTURER- manufacturer name 
# 5	CATEGORY- category of product
# 6	DESCRIPTION- description of product
# 18	 SUB_CATEGORY- sub-category of product
# 23	 PRODUCT_SIZE- package size of quantity of product



## Glossary data
glossary = pd.read_excel('/Users/zoezirlin/Desktop/Book5.xlsx')



## Reading the shapes and variable information for each set
transaction.shape
transaction.info()
#(472100, 12)
store.shape
store.info()
#(79, 9)
product.shape
product.info()
#(58, 6)






# =============================================================================
### Transaction Data Set ###


# What variables can predict units sold?
# What is the indicative difference between base price and price? Does that vary?
# Are units and visits correlated?
# Is week-end date a predictor for units sold? What are the most populous weeks for food shopping?
# Does display increase the units sold?
# Does spend increase as units sold does?



## Getting non-null counts
transaction.info()
# There are no null points in the dataframe, was cleaned prior to recieval



## Getting descriptive statistics for each variable
transaction_descriptives = transaction.describe()
# avg units purchased is 19.6, SD is 29.9, median is 10, max is 1800
# avg visits is 17.2, SD is 24.8, median is 9, max is 1340
# avg HHS is 16.8, SD is 24.2, median is 9, max is 1286
# avg spend is 53.22, SD is 68.4, median is 32, max is 2952
# avg price is 3.4, SD is 1.6, median is 3, max is 8.91
# avg base price is 3.6, SD is 1.6, median is 3.2, max is 11.46



## Visualization fonts
title_font = {'family':'Meiryo',
        'color':'teal',
        'weight':'normal',
        'size':16
        }

secondary_font = {'family':'Meiryo',
        'color':'teal',
        'weight':'normal',
        'size': 12
        }



## Looking to see if the variables are normally distributed
fig = plt.figure(figsize=(25,25))
ax = fig.gca()
transaction.hist(ax=ax)
plt.show()
# Not quite!



## X,Y plot- VISITS, UNITS
plt.plot('VISITS','UNITS', 
            marker='^',
            markersize=7,
            markerfacecolor='white',
            markeredgecolor='teal',
            data=transaction
            )
plt.title('Linear Relationship between Visits and Units Sold',fontdict=title_font)
plt.xlabel('Visits Made',fontdict=secondary_font)
plt.ylabel('Units Sold',fontdict=secondary_font)
plt.show()
# Very linear relationship



# X,Y plot- HHS, UNITS
plt.plot('HHS','UNITS',
         marker='^',
         markersize=7,
         markerfacecolor='grey',
         markeredgecolor='teal',
         data=transaction,
         )
plt.title('Linear Relationship between Households Purchased and Units Sold', fontdict=title_font)
plt.xlabel('House Holds Purchased', fontdict=secondary_font)
plt.ylabel('Units Sold', fontdict=secondary_font)
plt.show()
# Very linear relationship



# X,Y plot- PRICE, UNITS
plt.plot('PRICE','UNITS',
         marker='^',
         markersize=7,
         markerfacecolor='blue',
         markeredgecolor='teal',
         data=transaction
         )
plt.title('Linear Relationship between Price of Item and Units Sold', fontdict=title_font)
plt.xlabel('Price of Item', fontdict=secondary_font)
plt.ylabel('Units Sold', fontdict=secondary_font)
plt.show()
# Not a linear relationship



## Feature by units sold pivot table and bar plot
feature_pivot = pd.pivot_table(data=transaction, 
                               index=['FEATURE'],
                               values=['UNITS'])

feature_pivot_t = pd.pivot_table(data=transaction, 
                               index=['FEATURE'],
                               values=['UNITS']).plot(kind='bar')
# There are far more units sold when featured than not



## Display by units sold pivot table and bar plot
display_pivot = pd.pivot_table(data=transaction,
                               index=['DISPLAY'],
                               values=['UNITS'])

display_pivot_t = pd.pivot_table(data=transaction,
                               index=['DISPLAY'],
                               values=['UNITS']).plot(kind='bar')
# There are far more units sold when displayed than not



## TPR by units sold pivot table and bar plot
tpr_pivot = pd.pivot_table(data=transaction,
                           index=['TPR_ONLY'],
                           values=['UNITS'])

tpr_pivot_t = pd.pivot_table(data=transaction,
                           index=['TPR_ONLY'],
                           values=['UNITS']).plot(kind='bar')
# There are NOT more units sold when price temprorarily reduced



## Creating correlation table
transaction_correlation = transaction.corr(method = 'pearson')






# =============================================================================
### Store Data Set ###



## Checking for non-null values
store.info()
## Delete parking spaces variable because many null values



## Creating dummy variables for categorical variables
store['ADDRESS_STATE_PROV_CODE'] = store.ADDRESS_STATE_PROV_CODE.map({'IN':1,
                                                                      'KY':2,
                                                                      'OH':3,
                                                                      'TX':4
                                                                      })

store['ADDRESS_STATE_PROV_CODE'].value_counts()
# 4(TEXAS)    43
# 3(OHIO)     31
# 2(TEXAS)    4
# 1(INDIANA)  1



store['SEG_VALUE_NAME'] = store.SEG_VALUE_NAME.map({'VALUE':1,
                                                    'MAINSTREAM':2,
                                                    'UPSCALE':3
                                                    })

store['SEG_VALUE_NAME'].value_counts()
# 2(MAINSTREAM) 43
# 1(VALUE)      19
# 3(UPSCALE)    17





## Getting descriptive statistics for continuous variables
store_descriptives = store.describe()











# =============================================================================
### Product Data Set ###


## Creating dummy variables for categorical variables
product['MANUFACTURER'] = product.MANUFACTURER.map({'CHATTEM':1,
                                                    'COLGATE':2,
                                                    'FRITO LAY':4,
                                                    'GENERAL MI':5,
                                                    'HOME RUN':6,
                                                    'KELLOGG':7,
                                                    'KING':8,
                                                    'MKSL':9,
                                                    'P & G':10,
                                                    'POST FOODS':11,
                                                    'PRIVATE LABEL':12,
                                                    'QUAKER':13,
                                                    'SHULTZ':14,
                                                    'SNYDER S':15,
                                                    'TOMBSTONE':16,
                                                    'TONYS':17,
                                                    'WARNER':18
                                                    })

product['MANUFACTURER'].value_counts()
# 12 (PRIVATE LABEL)  12
# 18 (WARNER)         3
# 9 (MKSL)            3
# 4 (FRITO LAY)       3
# 5 (GENERAL MILLS)   3
# 6      3
# 7      3
# 8      3
# 10     3
# 17     3
# 11     3
# 13     3
# 14     3
# 15     3
# 16     3
# 1      3
# 2 (COLGATE)         1



product['CATEGORY'] = product.CATEGORY.map({'ORAL HYGIENE PRODUCTS':1,
                                            'BAG SNACKS':2,
                                            'COLD CEREAL':3,
                                            'FROZEN PIZZA':4,
                                            })

product['CATEGORY'].value_counts()
# 4 (FROZEN PIZZA)  15
# 3 (COLD CEREAL)   15
# 2 (BAG SNACKS)    15
# 1 (ORAL HYGIENE)  13



product['SUB_CATEGORY'] = product.SUB_CATEGORY.map({'ADULT CEREAL':1,
                                                    'ALL FAMILY CEREAL':2,
                                                    'KIDS CEREAL':3,
                                                    'MOUTHWASH/RINSES AND SPRAYS':4,
                                                    'MOUTHWASHES (ANTISEPTIC)':5,
                                                    'PIZZA/PREMIUM':6,
                                                    'PRETZELS':7
                                                    })

product['SUB_CATEGORY'].value_counts()











# =============================================================================
### Concatenating the three datasets ###

# Transactional as master set
# Importing products into transaction through UPC(I:21)
# Importing store into transaction through Store_Num(I:17)

# TRANSACTION+PRODUCTS=UPC
# TRANSACTION+STORE=STORE_NUM



















































## How much does advertising impact units sold?
X = transaction[['FEATURE','DISPLAY']]
y = transaction['UNITS']
X = sm.add_constant(X)
model_1 = sm.OLS(y,X).fit()
predictions_1 = model_1.predict(X)
model_1.summary()
























#NOTES AND IDEAS
## Drop unimportant/uninteresting columns
## Concatenate data 










