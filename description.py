import streamlit as st
import pandas as pd
import io

#df = pd.read_csv('data.csv')

def description(df):
    st.markdown("""
    <h3 style="color:Tomato;">DATAFRAME</h3>
    """, unsafe_allow_html=True)
    st.dataframe(df.head())
    st.markdown('---')
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("""
    <h3 style="color:Tomato;">FIELDS DESCRIPTION</h3>
    """, unsafe_allow_html=True)
        st.markdown("""
    - make: make of a car (BMW, Toyota, and so on)
    - model: model of a car
    - year: year when the car was manufactured
    - engine_fuel_type: type of fuel the engine needs (diesel, electric, and so on)
    - engine_hp: horsepower of the engine
    - engine_cylinders: number of cylinders in the engine
    - transmission_type: type of transmission (automatic or manual)
    - driven_wheels: front, rear, all
    - number_of_doors: number of doors a car has
    - market_category: luxury, crossover, and so on
    - vehicle_size: compact, midsize, or large
    - vehicle_style: sedan or convertible
    - highway_mpg: miles per gallon (mpg) on the highway
    - city_mpg: miles per gallon in the city
    - popularity: number of times the car was mentioned in a Twitter stream
    - msrp: manufacturer’s suggested retail price
        """)
    with col2:
        buffer = io.StringIO()
        df.info(buf=buffer)
        s = buffer.getvalue()
        st.markdown("""
    <h3 style="color:Tomato;">DATAFRAME INFO</h3>
    """, unsafe_allow_html=True)
        st.text(s)

    st.markdown("""
    <h3 style="color:Tomato;">DATAFRAME DESCRIBE</h3>
    """, unsafe_allow_html=True)
    st.dataframe(df.describe())