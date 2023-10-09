import redis
import datetime
import pymongo
import json
import sys
import time
from time import sleep
import os
from datetime import datetime
from datetime import timedelta
import pandas as pd
import math
import numpy as np
import scipy
from scipy.stats import norm
from scipy import sqrt, log, exp

N = norm.cdf
r=redis.Redis(host='localhost', port=6379,db=6, decode_responses= True)


################____________funtion for black_scholes_call_____________________________#######################################

def black_scholes_call(S, X, T, r, sigma):
    d1 = (math.log(S/X) + (r + sigma**2/2) * T) / (sigma * math.sqrt(T))
    d2 = d1 - sigma * math.sqrt(T)
    call_value = S * norm.cdf(d1) - X * math.exp(-r * T) * norm.cdf(d2)
    return call_value


################____________funtion for black_scholes_put________________________________#####################################

def black_scholes_put(S, X, T, r, sigma):
    d1 = (np.log(S/X) + (r + sigma**2/2)*T) / (sigma * np.sqrt(T))
    d2 = d1 - sigma * np.sqrt(T)
    return X * np.exp(-r*T) * N(-d2) - S * N(-d1)


################____________funtion to calculate IV for call_______________________#######################################    


def implied_volatility_call(S, X, T, r, call_price, sigma_estimate=0.2, tol=1e-5, max_iter=100):
    i = 0
    print(S, X, T, r, call_price)
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
        return 0.0
    else:
        return sigma
    
################______________funtion to calculate IV for put______________________________#########    

def implied_volatility_put(S, X, T, r, put_price, sigma_estimate=0.2, tol=1e-5, max_iter=100):
    i = 0
    print("hello")
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
        return 0.0
    else:
        return sigma

################________________functions to calculate delta____________________________#######################################

# def calculate_delta_method1_call(option_price, strike_price, underlying_price, time_to_expiry, interest_rate, volatility):
#     d1 = (math.log(underlying_price / strike_price) + (interest_rate + 0.5 * volatility**2) * time_to_expiry) / (volatility * math.sqrt(time_to_expiry))
#     delta = math.exp(-interest_rate * time_to_expiry) * norm.cdf(d1)
#     return delta

# def calculate_delta_method1_put(S, K, r, sigma, T):
#     d1 = (np.log(S/K) + (r + 0.5*sigma**2)*T) / (sigma*math.sqrt(T))
#     delta = -norm.cdf(-d1)
#     return delta


def calculate_delta_method1_call( S, X , T, rate, sigma):
    d1 = (math.log(S / X) + (rate + 0.5 * sigma**2) * T) / (sigma * math.sqrt(T))
    delta = math.exp(-rate * T) * norm.cdf(d1)
    return delta

def calculate_delta_method1_put(S, K, r, sigma, T):
    d1 = (np.log(S/K) + (r + 0.5*sigma**2)*T) / (sigma*math.sqrt(T))
    delta = -norm.cdf(-d1)
    return delta

################___________ function to get expiration time remaining_____________________________#######################################

def get_expiration_time_remaining():

    myclient = pymongo.MongoClient("mongodb://192.168.1.110:27017")
    mydb = myclient["Details"]
    coll = mydb['expiries']
    temp = coll.find_one()
    current_exp = datetime.strptime(temp["current"], "%Y-%m-%d")
    current_exp=current_exp+timedelta(hours=15.5)
    days=((current_exp-datetime.today()).days)
    hours=((current_exp-datetime.today()).seconds/(60*60))
    days=days+hours/24
    return days

