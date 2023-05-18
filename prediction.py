#import pickle as pk
import pandas as pd

with open('car_price_prediction.bin', 'rb') as f_in:
    sc, rf,_,_,_,_ = pd.read_pickle(f_in)    

def predict_single(df_params,df):
    cat_features = ['make', 'model', 'engine_fuel_type', 'transmission_type', 'driven_wheels', 'vehicle_size', 'vehicle_style','market_category']
    data_test = pd.concat([df_params,df], axis=0)
    cars_data = pd.get_dummies(data_test, columns = cat_features)
    X_testing= sc.fit_transform(cars_data)
    X_testing = X_testing[0].reshape(1, -1)
    pred = rf.predict(X_testing)
    return f"Car price prediction ($) --> {round(pred[0],2)}"
