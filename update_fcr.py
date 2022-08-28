import os
import pandas as pd
import matplotlib.pyplot as plt
import plotly.graph_objects as go
from plotly.subplots import make_subplots


token = os.environ.get("MY_SECRET_TOKEN")
if not token:
  raise RuntimeError("MY_SECRET_TOKEN env var is not set!")
print("All good! we found our env var")





data = pd.read_csv("https://bit.ly/3wrY3lV", sep=";")
print(data.info())




######################### CONCATENATE DATE & TIME COLUMNS (two methods, but diffferent dtype) v#########################
# https://stackoverflow.com/questions/17978092/combine-date-and-time-columns-using-python-pandas

# Method 1 (dtype: object)
# Datetime = data['Date'] + " " + data['Time']                          #dtype: object
# Method 2 (dtype: datetime64[ns])
data['Datetime'] = pd.to_datetime(data['Date'] + " " + data['Time'])    #dtype: datetime64[ns]

data["Unnamed: 5"] = data["Price"] * 2
data.rename({'Price': 'Price0,5h', 'Unnamed: 5': 'Price1h'}, axis=1, inplace=True)
data.drop(['Price0,5h', 'Direction'], axis=1, inplace=True)



######################### SAVE NEW TABLE AS A CSV ######################### 

data.to_csv("_export/dataLW.csv")


print("This is a test1")


######################### SIMPLE PLOT GRAPH #########################

plt.plot(data['Price1h'])
#plt.axis([0, 30000, 0, 520])
plt.ylabel('Price [€/MW per h]')
plt.show()


######################### Create HTML Interactiv Graph for website #########################
#########################  figure with secondary y-axis            #########################


fig = go.Figure()
fig = make_subplots(specs=[[{"secondary_y": True}]])

fig.add_trace(go.Scatter(x=data["Datetime"],y=data["Price1h"],name="Price1h"), secondary_y=False,)
fig.add_trace(go.Scatter(x=data["Datetime"],y=data["Value"],name="Power"), secondary_y=True,)
fig.update_layout(hovermode="x unified")
fig.update_layout(
    title="FCR Interactive Graph",
 #   xaxis_title="Time (h)",
 #   yaxis_title="FCR Price [€/MW per h]",
    legend=dict(
    yanchor="top",
    y=0.99,
    xanchor="left",
    x=0.01))

fig.update_yaxes(title_text="<b>Price</b> [€/MW per h]", secondary_y=False, range=[0,400])
fig.update_yaxes(title_text="<b>Total demand</b> [MW]", secondary_y=True, range=[0,700])
fig.show()

 

######################### SAVE HTML Interactiv Graph for website #########################
fig.write_html("graph_FCR.html")

######################### Create table with summary of information #########################
######################### create dataframe with describe.          #########################

data.describe().index
data.describe().columns
dd = data.describe()

######################### Save table with summary of information #########################
dd.to_html("table_FCR.html")
