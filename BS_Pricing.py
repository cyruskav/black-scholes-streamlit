# import necessary packages
import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from math import log,  exp
from scipy.stats import norm

# set Streamlit title
st.set_page_config(layout="wide")
st.title("Black Scholes European Option Pricer")

# Returns tuple of Call and Put B-S prices, given inputs
def BlackScholes (r, S0, K, T, sig):
    d1 = (log(S0/K) + (r + ((sig**2)/2)) * T) / (sig * np.sqrt(T))          # calculate d1
    d2 = d1 - sig*np.sqrt(T)                                                # calculate d2

    call_price = (S0 * norm.cdf(d1)) - (K * exp(-r*T) * norm.cdf(d2))       # Call B-S formula
    put_price = (K * exp(-r*T) * norm.cdf(-d2)) - (S0 *  norm.cdf(-d1))     # Put B-S formula

    return call_price, put_price

# Returns dataframes of call and put prices for a range of volatilities and spot prices
def near_BS (r, S0, K, T, sig):
    # initialize call and put dataframes
    call_df = pd.DataFrame(0.0, index=range(11), columns=range(11))
    put_df = pd.DataFrame(0.0, index=range(11), columns=range(11))
    
    # label columns and rows with respective parameter
    column_labels = [round(S0*(0.8 + (0.04*i)), 2) for i in range(11)]
    row_labels = [round(sig*(0.5 + (.1*j)), 2) for j in range(11)]
    call_df.columns = column_labels
    call_df.index = row_labels
    put_df.columns = column_labels
    put_df.index = row_labels

    # loop through each cell and calculate call and put prices 
    for i in range(11):
        for j in range(11):
            S0_temp = round(S0*(0.8 + (0.04*i)), 2)
            sig_temp = round(sig*(0.5 + (.1*j)), 2)

            call_df.iloc[j, i] = round(BlackScholes(r, S0_temp, K, T, sig_temp)[0], 2)
            put_df.iloc[j, i] = round(BlackScholes(r, S0_temp, K, T, sig_temp)[1], 2)
    
    return call_df, put_df

# gather user inputs
S0 = st.sidebar.number_input("Spot Price", 0.0, 10000.0, 100.0, step=0.25)              # spot price
K = st.sidebar.number_input("Strike Price", 0.0, 10000.0, 100.0, step=0.25)             # strike price
sig = st.sidebar.number_input("Volatility", 0.0, 100.0, 0.2, step=0.01)                 # volatility
T = st.sidebar.number_input("Time to maturity (in years)", 0.0, 5.0, 1.0, step=0.1)     # time to maturity (in years)
r = st.sidebar.number_input("Risk-Free Interest Rate", 0.0, 0.5, 0.05, step=0.01)       # risk-free interest rate

# call functions
call_df, put_df = near_BS(r, S0, K, T, sig)
call_val, put_val = BlackScholes(r, S0, K, T, sig)
st.subheader("Black-Scholes Price at Inputs:")

# visualize heat maps
col1, col2 = st.columns(2)
with col1:  # call option
    st.metric(label="`Call Option Value`", value=f"${call_val:.2f}")
    st.subheader("Call Value - Heatmap")
    fig1, ax1 = plt.subplots(figsize=(9, 7))
    sns.heatmap(call_df, ax=ax1, cmap="RdYlGn", annot=True, fmt=".2f", annot_kws={"size": 8})
    ax1.set_title("Call Prices")
    ax1.set_xlabel("Spot Price")
    ax1.set_ylabel("Volatility")
    st.pyplot(fig1)
with col2:  # put option
    st.metric(label="`Put Option Value`", value=f"${put_val:.2f}")
    st.subheader("Put Value - Heatmap")
    fig2, ax2 = plt.subplots(figsize=(9, 7))
    sns.heatmap(put_df, ax=ax2, cmap="RdYlGn", annot=True, fmt=".2f", annot_kws={"size": 8})
    ax2.set_title("Put Prices")
    ax2.set_xlabel("Spot Price")
    ax2.set_ylabel("Volatility")
    st.pyplot(fig2)