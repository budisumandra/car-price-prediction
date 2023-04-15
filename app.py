import streamlit as st
import pandas as pd
from pathlib import Path
from description import description
from accuracy_R2 import score, score_visualize, score_compare
from prediction import predict_single
import warnings
warnings.filterwarnings('ignore')

current_dir = Path(__name__).parent if '__file__' in locals() else Path.cwd() 
css_file = current_dir/ "styles" / "main.css"
dataset = current_dir/"car_cleaned.csv"
data_sample = current_dir/"data_sample.csv"

PAGE_TITLE = 'CAR PRICE PREDICTION'
PAGE_ICON = 'chart_with_upwards_trend'
st.set_page_config(page_title=PAGE_TITLE, page_icon=PAGE_ICON,)

with open(css_file) as f:
    st.markdown("<style>{}</style>".format(f.read()), unsafe_allow_html=True)

colors = ['#ECB365','#064663','#04293A',"#041C32"]
df_cleaned = pd.read_csv('car_cleaned.csv')
df_cleaned.columns = df_cleaned.columns.str.lower().str.replace(' ','_')
object_columns = list(df_cleaned.dtypes[df_cleaned.dtypes == 'object'].index)
for col in object_columns:
    df_cleaned[col] = df_cleaned[col].str.lower().str.replace(' ', '_')

df2 = df_cleaned.copy()
df2 = df2.drop('msrp', axis=1)

with st.sidebar:
    #st.image('https://img.freepik.com/free-vector/urban-racing-sticker-design_236756-445.jpg')
    st.header('CHOOSE MENU')
    menus = st.radio('',['Description','Accuracy','Prediction'])

if menus == 'Description':
    with open(dataset, 'rb') as data:
        csv = data.read()
    st.markdown("""
    <h3 style="color:Tomato;">DOWNLOAD DATASET</h3>
    """, unsafe_allow_html=True)
    st.download_button(
        label= '📄 Click Me!',
        data = csv,
        file_name = dataset.name,
        mime = 'application/octet-stream'
    )
    st.write(description(df_cleaned))
elif menus == 'Accuracy':
    st.markdown("""
    <h3 style="color:#FB2576;">Coefficient of Determination (R^2)</h3>
    """, unsafe_allow_html=True)
    st.write(score())
    st.markdown('---')
    st.markdown("""
    <h3 style="color:#FB2576;text-align:center">Predicted Vs Actual MSRP Value of Testing Dataset</h3>
    <br></br>
    """, unsafe_allow_html=True)
    st.write(score_visualize(df_cleaned, colors[0], 'testing'))
    st.markdown("""
    <br></br>
    <h3 style="color:#FB2576;text-align:center">Predicted Vs Actual MSRP Value of Validating Dataset</h3>
    <br></br>
    """, unsafe_allow_html=True)
    st.write(score_visualize(df_cleaned, colors[1], 'validating'))
    st.markdown("""
    <br></br>
    <h3 style="color:#FB2576;text-align:center">Testing Vs Validating MSRP Prediction Histogram</h3>
    <br></br>
    """, unsafe_allow_html=True)
    st.write(score_compare(colors1=colors[2], colors2=colors[0]))
else:
    st.sidebar.header('User Input Features')
    with open(data_sample, 'rb') as data:
        csv = data.read()
    st.sidebar.markdown("""
    <h3 style="color:Tomato;">Example CSV input file</h3>
    """, unsafe_allow_html=True)
    st.sidebar.download_button(
        label= '📄 Click Me!',
        data = csv,
        file_name = data_sample.name,
        mime = 'application/octet-stream'
    )
    
    uploaded_file = st.sidebar.file_uploader("Upload your Input CSV File", type=['csv'])
    if uploaded_file is not None:
        input_df = pd.read_csv(uploaded_file)
        st.sidebar.markdown("""
        <h3 style="color:#F7C04A;background-color: #3F497F;text-align:center">Close the 'x' sign to back into the list of input parameters</h3>
    """, unsafe_allow_html=True)
    else:
        def user_input_features():
            st.sidebar.markdown('**Parameters**')
            make = st.sidebar.selectbox('make',tuple(df_cleaned.make.value_counts().index))
            model = st.sidebar.selectbox('model',tuple(df_cleaned.model.value_counts().index))
            year = st.sidebar.slider('year',int(df_cleaned.year.min()),int(df_cleaned.year.max())+50)
            engine_fuel_type = st.sidebar.selectbox('engine_fuel_type',tuple(df_cleaned.engine_fuel_type.value_counts().index))
            engine_hp = st.sidebar.slider('engine_hp',float(df_cleaned.engine_hp.min()),float(df_cleaned.engine_hp.max()))
            engine_cylinders = st.sidebar.slider('engine_cylinders',float(df_cleaned.engine_cylinders.min()),float(df_cleaned.engine_cylinders.max()))
            transmission_type = st.sidebar.selectbox('transmission_type',tuple(df_cleaned.transmission_type.value_counts().index))
            driven_wheels = st.sidebar.selectbox('driven_wheels',tuple(df_cleaned.driven_wheels.value_counts().index))
            number_of_doors = st.sidebar.selectbox('number_of_doors',tuple(df_cleaned.number_of_doors.value_counts().index))
            market_category = st.sidebar.selectbox('market_category',tuple(df_cleaned.market_category.value_counts().index))
            vehicle_size = st.sidebar.selectbox('vehicle_size',tuple(df_cleaned.vehicle_size.value_counts().index))
            vehicle_style = st.sidebar.selectbox('vehicle_style',tuple(df_cleaned.vehicle_style.value_counts().index))
            highway_mpg = st.sidebar.slider('highway_mpg',float(df_cleaned.highway_mpg.min()),float(df_cleaned.highway_mpg.max()))
            city_mpg = st.sidebar.slider('city_mpg',float(df_cleaned.city_mpg.min()),float(df_cleaned.city_mpg.max()))
            popularity = st.sidebar.slider('popularity',float(df_cleaned.popularity.min()),float(df_cleaned.popularity.max()))

            params = dict()
            params['make'] = make
            params['model'] = model
            params['year'] = year
            params['engine_fuel_type'] = engine_fuel_type
            params['engine_hp'] = engine_hp
            params['engine_cylinders'] = engine_cylinders
            params['transmission_type'] = transmission_type
            params['driven_wheels'] = driven_wheels
            params['number_of_doors'] = number_of_doors
            params['market_category'] = market_category
            params['vehicle_size'] = vehicle_size
            params['vehicle_style'] = vehicle_style
            params['highway_mpg'] = highway_mpg
            params['city_mpg'] = city_mpg
            params['city_mpg'] = city_mpg
            params['popularity'] = popularity

            features_df = pd.DataFrame(params, index=[0])
            return features_df
        input_df = user_input_features()
    st.subheader('Data Input')
    st.write(input_df)
    st.subheader('Prediction:')
    st.write(predict_single(input_df,df2))