import os
import pandas as pd
import matplotlib.pyplot as plt
import plotly.graph_objects as go
import numpy as np
#import df2img
#from df2img import df2img
#from plotly.subplots import make_subplots
#import matplotlib as mpl

######################### TOKEN #########################
df = pd.DataFrame([[38.0, 2.0, 18.0, 22.0, 21, np.nan],[19, 439, 6, 452, 226,232]],
                  index=pd.Index(['Tumour (Positive)', 'Non-Tumour (Negative)'], name='Actual Label:'),
                  columns=pd.MultiIndex.from_product([['Decision Tree', 'Regression', 'Random'],['Tumour', 'Non-Tumour']], names=['Model:', 'Predicted:']))
print(df)
print(df.style)

######################### TEST df2img #########################
 
  
  
df = pd.DataFrame(
        {
            'Fruits': ['Apple', 'Apple', 'Apple', 'Orange', 'Banana', 'Orange'],
            'BuyPrice': [1000, 3000, 2400, 3000, 800, 1500],
            'SellPrice': [1200, 2800, 2500, 2500, 700, 1750]
        }
    )
    
    
# Display DataFrame
print('Original DataFrame:\n')
print(df)
    
# Add Profit percentage column
df['Profit'] = (df['SellPrice']-df['BuyPrice'])*100/df['BuyPrice']
df['Profit'] = df.apply(lambda x: "{:,.2f} %".format(x['Profit']), axis=1)
    
# Rename column titles
df = df.rename({'BuyPrice': 'Buy Price', 'SellPrice': 'Sell Price'}, axis=1)
    
# Highlight positive and negative profits
def highlight_cols(s):
  color = 'red' if type(s) != str and s < 0 else 'green'        
  return 'color: %s' % color
    
  df.style.applymap(highlight_cols, subset=['Profit'])


  print('\nFinal DataFrame:\n')
  print(df)
    
# Now create an image file for the table
    df2img(
        df,
        file="table_fruits.png",
        header_color="white",
        header_bgcolor="orange",
        row_bgcolors=["lightgray", "white"],
        font_size=10.0,
        col_width=1.5,
        row_height=0.3
    )
    
plt.show()

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


  
    
  
