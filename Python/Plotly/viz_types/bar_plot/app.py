import pandas as pd
import plotly
import plotly.express as px
import plotly.io as pio

# Import the data.
df = pd.read_csv("Caste.csv")
df = df[df['state_name'] == 'Maharashtra']
#df = df.groupby(['year', 'gender'], as_index=False)[['detenues', 'under_trial', 'convicts', 'others']].sum()
print(df.head())

# Create the plot.
barchart = px.bar(data_frame=df,
                  x="year",
                  y="convicts",
                  color="gender",
                  opacity=0.9,
                  orientation="v",
                  barmode="relative",
                  facet_col="caste",
                  facet_col_wrap=2,
                  
                  color_discrete_map={"Male":"gray", "Female":"red"},
                  
                  labels={"convicts":"Convicts in Maharashtra", 
                          "gender":"Gender"},
                          title="Indian Prison Statistics",
                          width=1400,
                          height=720,
                          template="gridon")

barchart.show()