import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.graph_objects as go 

colors = ['#ECB365','#064663','#04293A',"#041C32"]
def mean_price_per_year(df):
    index = df.groupby(['year']).mean()['msrp'].index.tolist()
    mean_per_year = df.groupby(['year']).mean()['msrp'].values.tolist()
    std_per_year = df.groupby(['year']).std()['msrp'].values.tolist()

    df_mean_price = pd.DataFrame(np.column_stack((mean_per_year,std_per_year)), columns=['mean','std'] ,index=index)
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=index,y=df_mean_price['mean'],
                            mode='markers', name='Mean Price', marker={'color':colors[0]}))
    fig.add_trace(go.Scatter(x=index,y=df_mean_price['std'],
                            mode='markers', name='Std Price', marker={'color':colors[1]}))

    reference_line = go.Scatter(x=[1988, df['year'].max()],
                                y=[20000, 20000],
                                mode="lines",
                                line=go.scatter.Line(color="red"),
                                showlegend=False)

    fig.add_trace(reference_line)

    fig.update_layout(title='Mean Price per Year',
                    xaxis_title='Year',
                    yaxis_title='std',
                    paper_bgcolor="LightSteelBlue")
    st.pyplot(fig)

def mean_price_per_brand(df):
    df_make_id = df.loc[df['make'].isin(df['make'].value_counts().head(10).index)]
    make_id_price = df_make_id.groupby('make')['msrp'].mean().round(0)\
    .astype('float64').sort_values(ascending=False)
    fig = plt.figure( figsize=(11,8))
    set_colors = [colors[1] if x in [56231.0,30493.0,29030.0] else colors[0] for x in make_id_price.values]
    fig = sns.barplot(data=pd.DataFrame(make_id_price).transpose(), orient = 'h', palette=set_colors)
    fig.set_title('Mean Price per Brand \n Range 1990-2017\n ', fontsize = 20)
    fig.set_ylabel('Brands', fontsize = 13)
    fig.set_xlabel('\nMean Price', fontsize = 13)
    fig.set_yticklabels(fig.get_yticklabels(), rotation=0)

    # Set the width and hight of annotation
    for p in fig.patches:
        width = p.get_width()
        if width in [56231.0,30493.0,29030.0]:
            clr = colors[0]
        else:
            clr = colors[1]
        plt.text(-5000+p.get_width(), p.get_y()+0.50*p.get_height(),
                '{:.0f}'.format(width) + ' US Dollar',color=clr,
                ha='center', va='center', fontsize = 'medium')
        
    sns.despine(right=True,top = True, left = True)
    plt.tight_layout()
    st.pyplot(fig);
