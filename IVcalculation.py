#!/usr/bin/env python
# coding: utf-8

# In[1]:


from IPython.display import display, HTML
display(HTML("<style>.container { width:98% !important; }</style>"))


# In[3]:


import time
import math
import numpy as np
import scipy
from scipy.stats import norm
# import pymongo
from datetime import datetime
from datetime import timedelta
# import redis
# import json
from scipy import sqrt, log, exp


# In[4]:


t1=time.time()
N = norm.cdf


# In[17]:


################____________funtion for black_scholes_call_____________________________#######################################

def black_scholes_call(S, X, T, r, sigma):
    d1 = (math.log(S/X) + (r + sigma**2/2) * T) / (sigma * math.sqrt(T))
    d2 = d1 - sigma * math.sqrt(T)
    call_value = S * norm.cdf(d1) - X * math.exp(-r * T) * norm.cdf(d2)
    return call_value


################____________funtion for black_scholes_put________________________________#####################################

def black_scholes_put(S, X, T, r, sigma):
    d1 = (math.log(S/X) + (r + sigma**2/2)*T) / (sigma * np.sqrt(T))
    d2 = d1 - sigma * np.sqrt(T)
    return X * np.exp(-r*T) * N(-d2) - S * N(-d1)


################____________funtion to calculate IV for call_______________________#######################################    


def implied_volatility_call(S, X, T, r, call_price, sigma_estimate=0.2, tol=1e-5, max_iter=1000):
    i = 0
    sigma = sigma_estimate
    option_value = black_scholes_call(S, X, T, r, sigma)
    diff = call_price - option_value
    
    while (abs(diff) > tol) and (i < max_iter):
        d1 = (np.lib.scimath.log(S/X) + (r + sigma**2/2) * T) / (sigma * np.lib.scimath.sqrt(T))
        vega = S * math.sqrt(T) * norm.pdf(d1)
        diff = call_price - option_value
        sigma = sigma + diff/vega
        option_value = black_scholes_call(S, X, T, r, sigma)
        i += 1
        
    if i == max_iter:
        print("Warning: maximum number of iterations reached for call iv calculation")
    return sigma

################______________funtion to calculate IV for put______________________________#########    

def implied_volatility_put(S, X, T, r, put_price, sigma_estimate=0.2, tol=1e-5, max_iter=1000):
    i = 0
    sigma = sigma_estimate
    option_value = black_scholes_put(S, X, T, r, sigma)
    diff = put_price - option_value
    while (abs(diff) > tol) and (i < max_iter):
        d1 = (math.log(S/X) + (r + sigma**2/2) * T) / (sigma * math.sqrt(T))
        vega = S * math.sqrt(T) * norm.pdf(d1)
        diff = put_price - option_value
        sigma = sigma + diff/vega
        option_value = black_scholes_put(S, X, T, r, sigma)
        i += 1
    if i == max_iter:
        print("Warning: maximum number of iterations reached for put iv calculation")
    return sigma

################________________functions to calculate delta____________________________#######################################


def calculate_delta_method1_call(strike_price, underlying_price, time_to_expiry, interest_rate, volatility):
    d1 = (math.log(underlying_price / strike_price) + (interest_rate + 0.5 * volatility**2) * time_to_expiry) / (volatility * math.sqrt(time_to_expiry))
    delta = math.exp(-interest_rate * time_to_expiry) * norm.cdf(d1)
    return delta

# S - Spot price
# K - Strike price of the option
# r = risk free rate
# sigma - volatility of the asset
# T - Time to expiry

def calculate_delta_method1_put(K, S, T, r, sigma):
    d1 = (np.log(S/K) + (r + 0.5*sigma**2)*T) / (sigma*math.sqrt(T))
    delta = -norm.cdf(-d1)
    return delta

# def calculate_delta_method2(ltp1, ltp2, underlying_ltp1, underlying_ltp2):
#     delta=(ltp2-ltp1)/( underlying_ltp2 - underlying_ltp1 )
#     return delta

################___________ function to get expiration time remaining_____________________________#######################################

def get_expiration_time_remaining():

    myclient = pymongo.MongoClient("mongodb://192.168.1.105:27017")
    mydb = myclient["Details"]
    coll = mydb['expiries']
    temp = coll.find_one()
    current_exp = datetime.strptime(temp["current"], "%Y-%m-%d")
    current_exp=current_exp+timedelta(hours=15.5)
    print(current_exp)
    days=((current_exp-datetime.today()).days)

    print(days)
    hours=((current_exp-datetime.today()).seconds/(60*60))
    print(hours)
    days=days+hours/24
    print(days)
    print("time to expiry {}".format(days))
    return days

################___________ function to get expiration time remaining_____________________________#######################################

def get_banknifty_index_price():

    RedisClientIndex=redis.Redis(host='localhost', port=6379,db=7, decode_responses= True)
    Banknifty_index_symbol="BankNifty"
    data_bn=RedisClientIndex.get(Banknifty_index_symbol)
    data_converted_bn=json.loads(data_bn)
    Banknifty_index_price=data_converted_bn['Touchline']['LastTradedPrice']
    return Banknifty_index_price

def get_nifty_index_price():
    RedisClientIndex=redis.Redis(host='localhost', port=6379,db=7, decode_responses= True)
    Nifty_index_symbol="Nifty50"
    data_Nifty=RedisClientIndex.get(Nifty_index_symbol)
    data_converted_nifty=json.loads(data_Nifty)
    nifty_index_price=data_converted_nifty['Touchline']['LastTradedPrice']
    return nifty_index_price

####################________calculating gamma__________________#################################

def d1(S, X, r, sigma, T):
    return (math.log(S / X) + (r + 0.5 * sigma**2) * T) / (sigma * math.sqrt(T))

def norm_pdf(x):
    return (1.0 / math.sqrt(2 * math.pi)) * math.exp(-0.5 * x**2)

def call_gamma(S, X, r, sigma, T):
    d1_val = d1(S, X, r, sigma, T)
    d2_val = d1_val - sigma * math.sqrt(T)
    return norm_pdf(d1_val) / (S * sigma * math.sqrt(T))

def put_gamma(S, X, r, sigma, T):
    d1_val = d1(S, X, r, sigma, T)
    d2_val = d1_val - sigma * math.sqrt(T)
    return norm_pdf(d1_val) / (S * sigma * math.sqrt(T))


################____________________________________________#######################################


def calculate_theta_call(S, K, r, sigma, T):
    d1 = (math.log(S/K) + (r + 0.5*sigma**2)*T) / (sigma*math.sqrt(T))
    d2 = d1 - sigma*math.sqrt(T)
    theta = -((S*norm.pdf(d1)*sigma)/(2*math.sqrt(T))) - r*K*np.exp(-r*T)*norm.cdf(d2)
    return theta/365

def calculate_theta_put(S, K, r, sigma, T):
    d1 = (math.log(S/K) + (r + 0.5*sigma**2)*T) / (sigma*math.sqrt(T))
    d2 = d1 - sigma*math.sqrt(T)
    theta = -((S*norm.pdf(d1)*sigma)/(2*math.sqrt(T))) + r*K*np.exp(-r*T)*norm.cdf(-d2)
    return theta/365


# In[14]:


# S = 40834.65 #get_banknifty_index_price() # spot price of banknifty index
# T = 2.4#get_expiration_time_remaining()
# T= T/365
# r=0.1

# X=40900   #strike price
# call_price= 189.75
# put_price= 235.05

#S = 36631.3                #get_banknifty_index_price() # spot price of banknifty index
# T = 2.2569444444444446   #get_expiration_time_remaining()
# T= T/365
#T = 0.0061643835616438354
#r = 0.1

#X = 36000   #strike price
# call_price = 82.4
#put_price = 82.4

# 36469.6 36500 2.2569444444444446 0.1 283.5
# Delta parameters:  36469.6 37100 0.006183409436834095 0.1 83.7


# In[18]:


# sigma_call = implied_volatility_call(S, X, T, r, call_price)
#sigma_put = implied_volatility_put(S, X, T, r, put_price)


# delta_call=calculate_delta_method1_call (X, S, T, r, sigma_call)
#delta_put = calculate_delta_method1_put(X, S, T, r, sigma_put)

#sigma_put, delta_put


# In[7]:


#sigma_call = implied_volatility_call(S, X, T, r, call_price)
# sigma_put = implied_volatility_put(S, X, T, r, put_price)


#delta_call=calculate_delta_method1_call (X, S, T, r, sigma_call)
# delta_put=calculate_delta_method1_put(S, X, r, sigma_put, T)


#gamma_call= call_gamma(S, X, r, sigma_call, T)
#gamma_put= call_gamma(S, X, r, sigma_put, T)


#theta_call=calculate_theta_call(S, X, r, sigma_call, T)
#theta_put=calculate_theta_put(S, X, r, sigma_put, T)


#print("IV call ",sigma_call)
#print("IV put",sigma_put)

#print("delta call", round(delta_call, 2))
#print("delta put", round(delta_put, 2))

#print("Gamma call:", gamma_call)
#print("Gamma put:", gamma_put)

#print("theta call", theta_call)
#print("theta put", theta_put)


# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:




