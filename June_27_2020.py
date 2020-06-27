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

## Research questions for the 57 products
# What variables can predict units sold?
# What is the difference between base price and price? Does that vary?
# Is units and visits correlated?
# Is week-end date a predictor for units sold? What are the most populous weeks for food shopping?
# Does display increase the units sold?
# Does spend increase as units sold does?



## Getting non-null counts
transaction.info()
# There are no null points in the dataframe



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
                               values=['UNITS']).plot(kind='bar', 
                                                      color='teal',
                                                      title='Do Units Purchased vary by Feature Status?'
                                                      )
# There are far more units sold when featured than not



## Display by units sold pivot table and bar plot
display_pivot = pd.pivot_table(data=transaction,
                               index=['DISPLAY'],
                               values=['UNITS'])

display_pivot_t = pd.pivot_table(data=transaction,
                               index=['DISPLAY'],
                               values=['UNITS']).plot(kind='bar',
                                                      color='teal',
                                                      title='Do Units Purchased vary by Display Status?'
                                                      )
# There are far more units sold when displayed than not



## TPR by units sold pivot table and bar plot
tpr_pivot = pd.pivot_table(data=transaction,
                           index=['TPR_ONLY'],
                           values=['UNITS'])

tpr_pivot_t = pd.pivot_table(data=transaction,
                           index=['TPR_ONLY'],
                           values=['UNITS']).plot(kind='bar',
                                                  color='teal',
                                                  title='Do Units Purchased vary by TPR Status?',
                                                  )
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
### Concatenating the three data frames ###

# Transactional as master set
# Importing products into transaction through UPC(I:21)
# Importing store into transaction through Store_Num(I:17)

# TRANSACTION+PRODUCTS=UPC
# TRANSACTION+STORE=STORE_NUM

# TRANSACTION+PRODUCTS=UPC

# merge() for combining data on common columns or indices
# .join() for combining data on a key column or an index

# left data frame: transaction    right data frame: products
# key column: UPC
# inner join: UPC
# you need a full outter join


inner_merged = pd.merge(transaction, product, on=['UPC'])
data = pd.merge(inner_merged, store, on=['STORE_ID'])



data.info()
# 24 predictor variables/columns
# 1 response variable/column (UNITS)
data_corr = data.corr(method = 'pearson')






# =============================================================================
### Analyzing full data set ###



## Boxplots to analyze effects of cat. var. on units sold

#matplotlib.pyplot.boxplot(data, notch=None, vert=None, patch_artist=None, widths=None)
# plt.boxplot('UNITS', 'CATEGORY', 
#             data = data, ,
#             )
# plt.title('Boxplot for Categories by Units Sold',fontdict=title_font)
# plt.xlabel('Food Categories',fontdict=secondary_font)
# plt.ylabel('Units Sold',fontdict=secondary_font)
# plt.show()


# Pivot tables


# Modeling functions
# 1. Logistic- predicting display as a function of category, brand, subcategory, price
# 2. Logitstic- predicting feature as a function of category, brand, subcategory, price
# 3. Linear- predicting HHS as a function of cateogery, brand, subcategory, price
# 4. Linear- predicting units as a function of promotion and feature
# 5. Linear- predicting sales as a function of seg value






# 1. Logistic- predicting display as a function of category, brand, subcategory, price
X = data[['MANUFACTURER','CATEGORY','SUB_CATEGORY']]
y = data['DISPLAY']
X = sm.add_constant(X)
model_1 = sm.OLS(y,X).fit()
predictions_1 = model_1.predict()
model_1.summary()


#                             OLS Regression Results                            
# ==============================================================================
# Dep. Variable:                DISPLAY   R-squared:                       0.015
# Model:                            OLS   Adj. R-squared:                  0.015
# Method:                 Least Squares   F-statistic:                     2501.
# Date:                Sat, 27 Jun 2020   Prob (F-statistic):               0.00
# Time:                        14:22:56   Log-Likelihood:            -1.2127e+05
# No. Observations:              484427   AIC:                         2.425e+05
# Df Residuals:                  484423   BIC:                         2.426e+05
# Df Model:                           3                                         
# Covariance Type:            nonrobust                                         
# ================================================================================
#                    coef    std err          t      P>|t|      [0.025      0.975]
# --------------------------------------------------------------------------------
# const           -0.0288      0.002    -16.181      0.000      -0.032      -0.025
# MANUFACTURER     0.0056      0.000     52.476      0.000       0.005       0.006
# CATEGORY         0.0109      0.000     24.884      0.000       0.010       0.012
# SUB_CATEGORY     0.0106      0.000     45.146      0.000       0.010       0.011
# ==============================================================================
# Omnibus:                   221326.239   Durbin-Watson:                   1.006
# Prob(Omnibus):                  0.000   Jarque-Bera (JB):           809405.898
# Skew:                           2.430   Prob(JB):                         0.00
# Kurtosis:                       7.059   Cond. No.                         52.7
# ==============================================================================

# Warnings:
# [1] Standard Errors assume that the covariance matrix of the errors is correctly specified.
# """






# 2. Logitstic- predicting feature as a function of category, brand, subcategory, price
X = data[['MANUFACTURER','CATEGORY','SUB_CATEGORY']]
y = data['FEATURE']
X = sm.add_constant(X)
model_2 = sm.OLS(y,X).fit()
predictions_2 = model_2.predict()
model_2.summary()

#                             OLS Regression Results                            
# ==============================================================================
# Dep. Variable:                FEATURE   R-squared:                       0.028
# Model:                            OLS   Adj. R-squared:                  0.028
# Method:                 Least Squares   F-statistic:                     4724.
# Date:                Sat, 27 Jun 2020   Prob (F-statistic):               0.00
# Time:                        14:24:16   Log-Likelihood:                -60498.
# No. Observations:              484427   AIC:                         1.210e+05
# Df Residuals:                  484423   BIC:                         1.210e+05
# Df Model:                           3                                         
# Covariance Type:            nonrobust                                         
# ================================================================================
#                    coef    std err          t      P>|t|      [0.025      0.975]
# --------------------------------------------------------------------------------
# const           -0.0430      0.002    -27.378      0.000      -0.046      -0.040
# MANUFACTURER     0.0046   9.39e-05     49.114      0.000       0.004       0.005
# CATEGORY         0.0362      0.000     93.940      0.000       0.035       0.037
# SUB_CATEGORY    -0.0032      0.000    -15.198      0.000      -0.004      -0.003
# ==============================================================================
# Omnibus:                   272642.947   Durbin-Watson:                   1.477
# Prob(Omnibus):                  0.000   Jarque-Bera (JB):          1522453.653
# Skew:                           2.861   Prob(JB):                         0.00
# Kurtosis:                       9.534   Cond. No.                         52.7
# ==============================================================================

# Warnings:
# [1] Standard Errors assume that the covariance matrix of the errors is correctly specified.
# """






# 3. Linear- predicting HHS as a function of cateogery, brand, subcategory, price
X = data[['CATEGORY','MANUFACTURER','SUB_CATEGORY','PRICE']]
y = data['HHS']
X = sm.add_constant(X)
model_3 = sm.OLS(y,X).fit()
predictions_3 = model_3.predict(X)
model_3.summary()

#                             OLS Regression Results                            
# ==============================================================================
# Dep. Variable:                    HHS   R-squared:                       0.182
# Model:                            OLS   Adj. R-squared:                  0.182
# Method:                 Least Squares   F-statistic:                 2.692e+04
# Date:                Sat, 27 Jun 2020   Prob (F-statistic):               0.00
# Time:                        14:27:32   Log-Likelihood:            -2.1811e+06
# No. Observations:              484427   AIC:                         4.362e+06
# Df Residuals:                  484422   BIC:                         4.362e+06
# Df Model:                           4                                         
# Covariance Type:            nonrobust                                         
# ================================================================================
#                    coef    std err          t      P>|t|      [0.025      0.975]
# --------------------------------------------------------------------------------
# const           31.8322      0.128    247.843      0.000      31.580      32.084
# CATEGORY         6.0348      0.032    186.511      0.000       5.971       6.098
# MANUFACTURER    -0.4097      0.007    -54.631      0.000      -0.424      -0.395
# SUB_CATEGORY    -1.6789      0.017   -100.556      0.000      -1.712      -1.646
# PRICE           -5.2741      0.022   -244.053      0.000      -5.316      -5.232
# ==============================================================================
# Omnibus:                   600304.103   Durbin-Watson:                   0.642
# Prob(Omnibus):                  0.000   Jarque-Bera (JB):        231776828.284
# Skew:                           6.412   Prob(JB):                         0.00
# Kurtosis:                     109.388   Cond. No.                         55.7
# ==============================================================================

# Warnings:
# [1] Standard Errors assume that the covariance matrix of the errors is correctly specified.
# """






# 4. Linear- predicting units as a function of display and feature
X = data[['FEATURE','DISPLAY']]
y = data['UNITS']
X = sm.add_constant(X)
model_4 = sm.OLS(y,X).fit()
predictions_4 = model_4.predict(X)
model_4.summary()

#                             OLS Regression Results                            
# ==============================================================================
# Dep. Variable:                  UNITS   R-squared:                       0.132
# Model:                            OLS   Adj. R-squared:                  0.132
# Method:                 Least Squares   F-statistic:                 3.692e+04
# Date:                Sat, 27 Jun 2020   Prob (F-statistic):               0.00
# Time:                        14:29:51   Log-Likelihood:            -2.2992e+06
# No. Observations:              484427   AIC:                         4.598e+06
# Df Residuals:                  484424   BIC:                         4.598e+06
# Df Model:                           2                                         
# Covariance Type:            nonrobust                                         
# ==============================================================================
#                  coef    std err          t      P>|t|      [0.025      0.975]
# ------------------------------------------------------------------------------
# const         15.3733      0.043    357.376      0.000      15.289      15.458
# FEATURE       22.7418      0.158    144.262      0.000      22.433      23.051
# DISPLAY       21.1948      0.140    151.396      0.000      20.920      21.469
# ==============================================================================
# Omnibus:                   615187.779   Durbin-Watson:                   0.610
# Prob(Omnibus):                  0.000   Jarque-Bera (JB):        328292417.057
# Skew:                           6.595   Prob(JB):                         0.00
# Kurtosis:                     129.849   Cond. No.                         4.49
# ==============================================================================

# Warnings:
# [1] Standard Errors assume that the covariance matrix of the errors is correctly specified.
# """






# 5. Linear- predicting units as a function of seg value
X = data['SEG_VALUE_NAME']
y = data['UNITS']
X = sm.add_constant(X)
model_5 = sm.OLS(y,X).fit()
predictions_5 = model_5.predict(X)
model_5.summary()

#                             OLS Regression Results                            
# ==============================================================================
# Dep. Variable:                  UNITS   R-squared:                       0.007
# Model:                            OLS   Adj. R-squared:                  0.007
# Method:                 Least Squares   F-statistic:                     3239.
# Date:                Sat, 27 Jun 2020   Prob (F-statistic):               0.00
# Time:                        14:36:13   Log-Likelihood:            -2.3319e+06
# No. Observations:              484427   AIC:                         4.664e+06
# Df Residuals:                  484425   BIC:                         4.664e+06
# Df Model:                           1                                         
# Covariance Type:            nonrobust                                         
# ==================================================================================
#                      coef    std err          t      P>|t|      [0.025      0.975]
# ----------------------------------------------------------------------------------
# const             12.2359      0.137     89.424      0.000      11.968      12.504
# SEG_VALUE_NAME     3.6757      0.065     56.911      0.000       3.549       3.802
# ==============================================================================
# Omnibus:                   627727.472   Durbin-Watson:                   0.665
# Prob(Omnibus):                  0.000   Jarque-Bera (JB):        288398292.878
# Skew:                           6.932   Prob(JB):                         0.00
# Kurtosis:                     121.726   Cond. No.                         8.15
# ==============================================================================

# Warnings:
# [1] Standard Errors assume that the covariance matrix of the errors is correctly specified.
# """














#NOTES AND IDEAS
## Drop unimportant/uninteresting columns
## Concatenate data 










