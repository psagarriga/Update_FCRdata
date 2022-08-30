import os
import pandas as pd
import matplotlib.pyplot as plt
import plotly.graph_objects as go
import numpy as np
from pretty_html_table import build_table


#from plotly.subplots import make_subplots
#import matplotlib as mpl





def generate_table():
    df = pd.DataFrame(data={
        'ID' : [1,2,3,4],
        'First Name' : ['Flore', 'Grom', 'Truip', 'Ftro'],
        'Last Name' : ['Ju', 'Re', 'Ve', 'Cy'],
        'Age' : [23, 45, 67, 12],
        'Place of Birth' : ['France', 'USA', 'China', 'India'],
        'Date of Birth' : ['1996-10-04', '1974-10-10', '1952-04-07', '2007-10-06']
    })

    start = """<html><body>"""
    end = """ </body></html>"""

    output = start \
            + '<p style="font-family:Century Gothic;">blue_light<br /><p>' \
            + build_table(
                df, 
                'blue_light',
                width_dict=['10px','700px', '50px', '10px','200px', '50px'],
                conditions={
                    'Age': {
                        'min': 25,
                        'max': 60,
                        'min_color': 'red',
                        'max_color': 'green',
                    }
                }
                ) \
            + '<p style="font-family:Century Gothic;">blue_dark<br /><p>' \
            + build_table(df, 'blue_dark') \
            + '<p style="font-family:Century Gothic;">grey_light<br /><p>' \
            + build_table(df, 'grey_light') \
            + '<p style="font-family:Century Gothic;">grey_dark<br /><p>' \
            + build_table(df, 'grey_dark') \
            + '<p style="font-family:Century Gothic;">orange_light<br /><p>' \
            + build_table(df, 'orange_light') \
            + '<p style="font-family:Century Gothic;">orange_dark<br /><p>' \
            + build_table(df, 'orange_dark') \
            + '<p style="font-family:Century Gothic;">yellow_light<br /><p>' \
            + build_table(df, 'yellow_light') \
            + '<p style="font-family:Century Gothic;">yellow_dark<br /><p>' \
            + build_table(df, 'yellow_dark') \
            + '<p style="font-family:Century Gothic;">green_light<br /><p>' \
            + build_table(df, 'green_light') \
            + '<p style="font-family:Century Gothic;">green_dark<br /><p>' \
            + build_table(df, 'green_dark') \
            + '<p style="font-family:Century Gothic;">red_light<br /><p>' \
            + build_table(df, 'red_light') \
            + '<p style="font-family:Century Gothic;">red_dark<br /><p>' \
            + build_table(df, 'red_dark') \
            + end

    with open('example.html', 'w') as f:
        f.write(output)
        
        




if __name__ == "__main__":
    generate_table()

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


  
    
  
