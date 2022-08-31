import os #required for TOKEN
import pandas as pd
#import matplotlib.pyplot as plt
import plotly.graph_objects as go
#import numpy as np
from pretty_html_table import build_table
#from plotly.subplots import make_subplots
#import matplotlib as mpl

######################### TOKEN #########################
token = os.environ.get("MY_SECRET_TOKEN")
if not token:
  raise RuntimeError("MY_SECRET_TOKEN env var is not set!")
print("All good! we found our env var")



######################### READ DATA FROM LIKEWATT Link (API GOOGLE) #########################

#data = pd.read_csv("https://firebasestorage.googleapis.com/v0/b/likewatt-4bb4b.appspot.com/o/DataFCR%2FFcrMarket_2020.csv?alt=media&amp;token=51b85804-e29a-40cb-8efd-5d9c55e1faa4", sep=";")
data = pd.read_csv("https://bit.ly/3wrY3lV", sep=";")




######################### CONCATENATE DATE & TIME COLUMNS (two methods, but diffferent dtype) v#########################
# https://stackoverflow.com/questions/17978092/combine-date-and-time-columns-using-python-pandas

# Method 1 (dtype: object)
# Datetime = data['Date'] + " " + data['Time']                          #dtype: object
# Method 2 (dtype: datetime64[ns])
data['Datetime'] = pd.to_datetime(data['Date'] + " " + data['Time'])    #dtype: datetime64[ns]

data["Price1h"] = data["Price"] * 2 #"Price" is the 30min Price
data.rename({'Value': 'Demand'}, axis=1, inplace=True)
data.drop(['Price', 'Unnamed: 5','Direction'], axis=1, inplace=True)

data['Datetime_Index']=data['Datetime']
data.set_index('Datetime_Index', inplace=True)



##############################################################################################
########################  CREATE Short data Tables 1Day, 3Days & 90Days    ###################
##############################################################################################

data1D = data.last('1D')
data7D = data.last('7D')
data90D = data.last('90D')



##############################################################################################
########################  Save HTML FCR Price Graph "data"           #########################
##############################################################################################

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


fig1.write_html("graph_FCR_price_full.html")



##############################################################################################
#####################  Save HTML FCR Price Graph "data90D"            ########################
##############################################################################################

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

fig2.write_html("graph_FCR_price_90D.html")



##############################################################################################
#####################  Create summary table with Describe 1D, 7D & 90D   #####################
##############################################################################################


#data.describe().index
#data.describe().columns

dd1D = data1D.describe().applymap('{:,.2f}'.format)
dd7D = data7D.describe().applymap('{:,.2f}'.format)
dd90D = data90D.describe().applymap('{:,.2f}'.format)


##############################################################################################
######################### Create  Save 1D Data Table                  ########################
##############################################################################################

data1D=data1D.sort_values(by=['Datetime_Index'], ascending=False) #Sorting values by column 
data1D.reset_index(inplace=True)
data1Db = data1D[['Date', 'Time', 'Price1h']]


def generate_table():

    start = """<html><body>"""
    end = """ </body></html>"""

    output = start \
            + '<p style="font-family:Century Gothic;">Last 24h FCR Prices<br /><p>' \
            + build_table(data1Db, 'blue_dark') \
            + end       
 
    with open('table_48h_data.html', 'w') as f:
        f.write(output)

if __name__ == "__main__":
    generate_table()

##############################################################################################
######################### Create Save Summary Table 7D                  ######################
##############################################################################################

dd7D.reset_index(inplace=True)


def generate_table():

    start = """<html><body>"""
    end = """ </body></html>"""

    output = start \
            + '<p style="font-family:Century Gothic;">Summary Table last 7 days FCR Prices<br /><p>' \
            + build_table(dd7D, 'blue_dark') \
            + end       
 
    with open('table_7D_FCR_summary.html', 'w') as f:
        f.write(output)

if __name__ == "__main__":
    generate_table()

##############################################################################################    
######################### Create Save Summary Table 90D                  #####################
##############################################################################################

dd90D.reset_index(inplace=True)


def generate_table():

    start = """<html><body>"""
    end = """ </body></html>"""

    output = start \
            + '<p style="font-family:Century Gothic;">Summary Table last 90 days FCR Prices<br /><p>' \
            + build_table(dd90D, 'blue_dark') \
            + end       
 
    with open('table_90D_FCR_summary.html', 'w') as f:
        f.write(output)

if __name__ == "__main__":
    generate_table()    
    dd90D.reset_index(inplace=True)
    
    
 

  
