import streamlit as st
from sklearn.metrics import r2_score

import pickle as pk
import matplotlib.pyplot as plt
import seaborn as sns

with open('car_price_prediction.bin', 'rb') as f_in:
    sc, rf, y_test,rfr_pred_test,y_valid,rfr_pred_val = pk.load(f_in)  

def score():
    st.markdown(f'R^2 Testing Score: {r2_score(y_test, rfr_pred_test)}')
    st.markdown(f'R^2 Validating Score: {r2_score(y_valid, rfr_pred_val)}')

def score_visualize(df, colors, kind):
    if kind == 'validating':
        fig = plt.figure(figsize=(10,10))
        plt.ylabel("Predicted Value")
        sns.regplot(data=df,x=y_valid,y=rfr_pred_val, fit_reg=True,scatter_kws={"s": 100}, color=colors)
        st.pyplot(fig)
    else:
        fig = plt.figure(figsize=(10,10))
        plt.ylabel("Predicted Value")
        sns.regplot(data=df,x=y_test,y=rfr_pred_test, fit_reg=True,scatter_kws={"s": 100}, color=colors)
        st.pyplot(fig)

def score_compare(colors1, colors2):
    fig = plt.figure(figsize=(10,10))
    sns.histplot(rfr_pred_val, label='prediction_val', color=colors1)
    sns.histplot(rfr_pred_test, label='prediction_test',color=colors2)
    plt.legend()
    st.pyplot(fig)
