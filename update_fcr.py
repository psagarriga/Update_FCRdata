import os
import pandas as pd
import matplotlib.pyplot as plt
import plotly.graph_objects as go
from plotly.subplots import make_subplots

import pandas as pd
import numpy as np
import matplotlib as mpl

df = pd.DataFrame([[38.0, 2.0, 18.0, 22.0, 21, np.nan],[19, 439, 6, 452, 226,232]],
                  index=pd.Index(['Tumour (Positive)', 'Non-Tumour (Negative)'], name='Actual Label:'),
                  columns=pd.MultiIndex.from_product([['Decision Tree', 'Regression', 'Random'],['Tumour', 'Non-Tumour']], names=['Model:', 'Predicted:']))
df.style



######################### TOKEN #########################
token = os.environ.get("MY_SECRET_TOKEN")
if not token:
  raise RuntimeError("MY_SECRET_TOKEN env var is not set!")
print("All good! we found our env var")

######################### READ DATA FCR #########################

data = pd.read_csv("https://bit.ly/3wrY3lV", sep=";")


######################### CONCATENATE DATE & TIME COLUMNS #########################
data['Datetime'] = pd.to_datetime(data['Date'] + " " + data['Time'])    #dtype: datetime64[ns]

data["Price1h"] = data["Price"] * 2 #"Price" is the 30min Price
data.rename({'Value': 'Demand'}, axis=1, inplace=True)
data.drop(['Price', 'Unnamed: 5','Direction'], axis=1, inplace=True)

data['Datetime_Index']=data['Datetime']
data.set_index('Datetime_Index', inplace=True)

data1D = data.last('1D')
data90D = data.last('90D')


######################### Create HTML Interactiv Graph for website #########################

 
########################  FCR Price Graph            #########################

fig1 = go.Figure()
fig1.add_trace(go.Scatter(x=data["Datetime"],y=data["Price1h"],name="Price1h"))
fig1.update_layout(hovermode="x unified")
fig1.update_layout(
    title="FCR Settlement Price",
    xaxis_title="Time (h)",
    yaxis_title="FCR Settlement Price [€/MW per h]",
    legend=dict(
    yanchor="top",
    y=0.99,
    xanchor="left",
    x=0.01))

fig1.show()


#########################  FCR Price Graph 90D            #########################

fig2 = go.Figure()
fig2.add_trace(go.Scatter(x=data90D["Datetime"],y=data90D["Price1h"],name="Price1h"))
fig2.update_layout(hovermode="x unified")
fig2.update_layout(
    title="FCR Settlement Price last 90 days",
    xaxis_title="Time (h)",
    yaxis_title="FCR Settlement Price [€/MW per h]",
    legend=dict(
    yanchor="top",
    y=0.99,
    xanchor="left",
    x=0.01))

fig2.show()
  
  
######################### SAVE HTML Interactiv Graph for website #########################


fig1.write_html("graph_FCR_price.html")
fig2.write_html("graph_FCR_price_90D.html")

  
    
######################### SAVE Table as png                   #########################
  
  
data1D.reset_index(inplace=True)
data1Db = data1D[['Date', 'Time', 'Price1h']]


  
    
  
