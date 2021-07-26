#!/usr/bin/env python
# coding: utf-8

# In[30]:


import pandas as pd
import json
import matplotlib.pyplot as plt
from plotly.subplots import make_subplots
from matplotlib import style
get_ipython().run_line_magic('matplotlib', 'inline')
style.use('ggplot')
import plotly
import plotly.express as px
import plotly.graph_objects as go
import plotly.offline as pyo
import numpy as np
from datetime import datetime
import os


import cufflinks as cf
from plotly.offline import init_notebook_mode,plot,iplot

import folium


# In[31]:


#to print the graphs in the jupyter itself
pyo.init_notebook_mode(connected=True)
cf.go_offline()


# In[32]:


#reading statewise_covid_cases.xlsx file using pandas
df=pd.read_excel(r"C:\Users\nisha\Documents\python\python_projects\covid_19_analysis\covid-19_analysis_final\statewise_covid_cases.xlsx")
df


# In[33]:


df['State/UT']=df['State/UT'].str.upper() #converting all the data in stae/ut column to uppercase


# In[34]:


df


# In[35]:



total_confirmed_cases=df['Confirmed Cases'].sum() #summing up the total confirmed cases
print("Total Coronavirus Cases In India Is ",total_confirmed_cases)


# In[36]:


df.style.background_gradient(cmap='YlOrRd') #createing background style for interactive view


# In[37]:


df.style.background_gradient(cmap='YlOrRd',subset='Confirmed Cases')
#applying gradient in  only Confirmed Cases column using subset


# In[38]:


total_active=df.groupby('State/UT')['Active Cases'].sum().sort_values(ascending=False).to_frame()
# using groupy to see the data in group and sorting the values in descending order .at last
# converting it to data frame
total_active


# In[39]:


total_active.style.background_gradient(cmap='YlOrRd')


# In[40]:


#adding two more columns ,1. percentage recovery date 2. percentage mortality rate
df['Recovery Rate']=np.round((df['Cured/Discharged']/df['Confirmed Cases'])*100,2)
df['Mortality Rate']=np.round((df['Death']/df['Confirmed Cases'])*100,2)


# In[41]:


df


# In[ ]:






# In[42]:


fig = go.Figure() #creating figure object


fig.add_trace(go.Bar(
    x=df['State/UT'],
    y=df['Confirmed Cases'],
    marker=dict(
        color='rgba(50, 171, 96, 0.6)',#specifying the color of the graph
        line=dict(
            color='rgba(50, 171, 96, 1.0)',#specifying the color of the boundry of bars
            width=1),#setting the width of the line
    ),
    name='Confirmed Cases',
    
))







#width=set width of the line of bar graph

fig.update_layout(
    title='Total Confirmed Cases In India',yaxis=dict(showgrid=False,showline=False),
    autosize=False,
    width=800, #setting the width and height of graph for proper view
    height=850,
    xaxis=dict(zeroline=False,
        showline=False,
        showticklabels=True, 
        showgrid=False),paper_bgcolor='rgb(248, 248, 255)',#seeing the paper background color
    plot_bgcolor='rgb(248, 248, 255)',bargap=0.2)#setting the plot background color
#bargap=gap between two consecutive bars

fig.show()


# In[43]:


fig = go.Figure() #creating graph object

#creating two bar graphs in the same plot
#add trace to first graph
fig.add_trace(go.Bar(
    x=df['State/UT'],
    y=df['Confirmed Cases'],
    marker=dict(
        color='red'
        
    ),
    name='Confirmed Cases',
    
))



#add tarce for second graph
fig.add_trace(go.Bar(
    x=df['State/UT'],
    y=df['Active Cases'],
    name='Active Cases',
    marker=dict(
        color='blue',)
    )
)




fig.update_layout(
    title='Total Confirmed and Active Cases In India',yaxis=dict(showgrid=False,showline=False),
    autosize=False,
    width=800,
    height=850,
    xaxis=dict(zeroline=False,
        showline=False,
        showticklabels=True,
        showgrid=False),paper_bgcolor='rgb(248, 248, 255)',
    plot_bgcolor='rgb(248, 248, 255)',bargap=0.2
)
#bargap=gap between two consecutive bars
fig.update_layout(barmode='stack')
#use barmode='stack' to stack the bars
fig.show()








# In[44]:


fig = go.Figure(data=[
    go.Bar(name='Confirmed Cases', x=df['State/UT'],
    y=df['Confirmed Cases']),
    go.Bar(name='Cured', x=df['State/UT'], y=df['Cured/Discharged'])
])

fig.update_layout(
    title='Corona Stat Of India',yaxis=dict(showgrid=True,showline=False),
    autosize=False,
    width=900,
    height=600,
    xaxis=dict(zeroline=False,
        showline=True,
        showticklabels=True,
        showgrid=True),paper_bgcolor='rgb(248, 248, 255)',
    plot_bgcolor='rgb(248, 248, 255)',bargap=0.2
)


# Change the bar mode
fig.update_layout(barmode='group')
fig.show()


# In[45]:


df


# In[46]:


#creating 4 scatter plots using two y axis in the same plot

fig = make_subplots(specs=[[{"secondary_y": True}]]) #use subplots and assign secondary_y:true 


#trace for first scatter plot
fig.add_trace(go.Scatter(
    x=df['State/UT'],
    y=df['Confirmed Cases'],mode="lines+markers",
    name='Confirmed Cases(y-axis:1)'
    
),secondary_y=False)#setting secondary_y: false means it will use primary y-axis for plotting 

#adding trace for second scatter plot
fig.add_trace(go.Scatter(
    x=df['State/UT'],
    y=df['Cured/Discharged'],mode="lines+markers",
    name='Cured/Discharged(y-axis:1)',
    
),secondary_y=False)


#trace for third scatter plot
fig.add_trace(go.Scatter(
    x=df['State/UT'],
    y=df['Death'],mode="lines+markers",
    name='Death(y-axis:2)',
    
),secondary_y=True) #secondary_y:true means it will use secondary y-axis for plotting



#trace for fourth scatter plot
fig.add_trace(go.Scatter(
    x=df['State/UT'],
    y=df['Active Cases'],
    name='Active Cases(y-axis:2)',mode="lines+markers"
    ),secondary_y=True
)




fig.update_layout(
    title='Coronavirus Update',
    autosize=False,
    width=840,
    height=700
)

fig.show()






# In[47]:


df


# In[48]:


#ploting graph for mortality rate and recovery rate
fig = make_subplots(specs=[[{"secondary_y": True}]])

# Add traces for recovery
fig.add_trace(
    go.Scatter(x=df['State/UT'], y=df['Recovery Rate'], name="Recovery Rate",mode="lines+markers"),
    secondary_y=False,
)

#add trace for recovery
fig.add_trace(
    go.Scatter(x=df['State/UT'], y=df['Mortality Rate'], name="Mortality Rate",mode="lines+markers"),
    secondary_y=True,
)

# Add figure title
fig.update_layout(
    title_text="Mortality And Recovery Rate"
)

# Set x-axis title
fig.update_xaxes(title_text="STATE/UT")

# Set y-axes titles
fig.update_yaxes(title_text="<b>Recovery Rate(%)", secondary_y=False)
fig.update_yaxes(title_text="<b>Mortality Rate(%)</b>", secondary_y=True)

#update the size of the image
fig.update_layout(
    autosize=False,
    width=840,
    height=800
)

fig.show()


# In[49]:


print("Average Mortality Rate is "+ str(np.round(df['Mortality Rate'].mean(),0)))
print()
print("Average Recovery Rate is "+ str(np.round(df['Recovery Rate'].mean(),0)))


# In[50]:


df


# In[51]:


#creating pie chart with hole of 0.6

labels = ['Confirmed Cases','Active Cases','Death','Cured'] #labels of the pie chart
values = [df['Confirmed Cases'].sum(),df['Active Cases'].sum(),df['Death'].sum(),
          df['Cured/Discharged'].sum()]#values of the pie chart

# Use `hole` to create a donut-like pie chart
fig = go.Figure(data=[go.Pie(labels=labels, values=values, hole=.6)])
fig.show()


# In[52]:


#choropleth map
#reading states_india.geojson file for choropleth
india_states=json.load(open(r"C:\Users\nisha\Documents\python\python_projects\covid_19_analysis\covid-19_analysis_final\states_india.geojson",'r'))
india_states['features'][0] 
#will show features of a particular state,try to change the 
# index value you will get feature of other state


# In[53]:


india_states['features'][0]['properties']


# In[54]:


state_id_map={} 
# #creating dictionary for mapping with original dataframe here i have used state_code as values
# for mapping and st_nm for key of dictionary
for feature in india_states['features']:
    feature['id']=feature['properties']['state_code']
    state_id_map[feature['properties']['st_nm'].upper()]=feature['id']


# In[55]:


state_id_map


# In[56]:


df


# In[57]:


#performing the required processing of dataset 

df['State/UT'][df['State/UT']=='ANDAMAN AND NICOBAR ISLANDS']='ANDAMAN & NICOBAR ISLAND'
df['State/UT'][df['State/UT']=='ARUNACHAL PRADESH']='ARUNANCHAL PRADESH'
df['State/UT'][df['State/UT']=='DADRA AND NAGAR HAVELI AND DAMAN AND DIU']='DAMAN & DIU'
df['State/UT'][df['State/UT']=='DELHI']='NCT OF DELHI'
df['State/UT'][df['State/UT']=='JAMMU AND KASHMIR']='JAMMU & KASHMIR'
df.drop(index=17,axis=0,inplace=True)


# In[58]:


df['id']=df['State/UT'].apply(lambda x: state_id_map[x])
#creating id column in df using mapping of dictionary


# In[59]:


df


# In[60]:



df['Confirmed Cases(log10)']=np.log10(df['Confirmed Cases'])
#taking log value for better distribution of colors across regions


# In[61]:


fig=px.choropleth(df,locations='id',color='Confirmed Cases(log10)',#colorscale value
                  geojson=india_states,hover_name='State/UT',
                 hover_data=['Confirmed Cases','Death','Cured/Discharged'],#list od data that you want to see while hovering
                  title="Latest Coronavirus Update Across Different Regions Of India",
                  )
fig.update_geos(fitbounds='locations',visible=False)
#using fitbounds to show only india map otherwise if it is not used than it will show whole world map


# In[62]:


#reading India States-UTs.csv file
ind_coordinate=pd.read_csv(r'C:\Users\nisha\Documents\python\python_projects\covid_19_analysis\covid-19_analysis_final\india_latitude_longitude\India States-UTs.csv')


# In[63]:


ind_coordinate['State/UT']=ind_coordinate['State/UT'].str.upper() 
#converting to upper case for proper mapping
ind_coordinate


# In[64]:


df_for_map=df.merge(ind_coordinate,left_on='State/UT', right_on='State/UT')
df_for_map
#to merge two dataframe


# In[65]:


#setting location to get focus on india
map=folium.Map(location=[20,70],zoom_start=4,tiles='stamenterrain')
for lat,long,total_case,state in zip(df_for_map['Latitude'],df_for_map['Longitude'],
                                    df_for_map['Active Cases'],df_for_map['State/UT']):
    folium.CircleMarker(location=[lat,long],radius=total_case*0.001,#multiply with certain nos otherwise it will show bigger circle
                        popup=("<strong>State:<br><\strong>" +str(state).capitalize() +"<br>"+ "<strong>Total Case:<\strong><br>" +str(total_case)),
                       color="red",fill=True,fill_color="red",opacity=0.3).add_to(map)
    
    
map


# In[66]:


#reading file us-numbers-who-covid-analysis-QueryResult.csv
df_usa=pd.read_csv(r"C:\Users\nisha\Documents\python\python_projects\covid_19_analysis\covid-19_analysis_final\us-numbers-who-covid-analysis-QueryResult.csv")
df_usa.sort_values('date',ascending=True,axis=0,inplace=True) 
#sorting values by date
df_usa.head(300)


# In[67]:


df_usa['date']= pd.to_datetime(df_usa['date']) #converting to datetime

df_usa.tail()


# In[68]:


start_date = '2021-01-01' #specifying the start and end date for plotting graph of four countries
end_date = '2021-06-30'
mask = (df_usa['date'] >= start_date) & (df_usa['date'] <= end_date)

df_usa = df_usa.loc[mask]
df_usa.head()


# In[69]:


df_usa.tail()


# In[70]:


df_usa.info()


# In[80]:


#reading file covid_19_sg.csv
df_singapore=pd.read_csv(r'C:\Users\nisha\Documents\python\python_projects\covid_19_analysis\covid-19_analysis_final\covid_19_sg.csv')
df_singapore.head(300)


# In[72]:


df_singapore['date']= pd.to_datetime(df_singapore['date'])
mask = (df_singapore['date'] >= start_date) & (df_singapore['date'] <= end_date)
df_singapore = df_singapore.loc[mask]
df_singapore.head()


# In[73]:


df_singapore.tail()


# In[77]:


# reading  file owid-covid-data.csv
df_for_all_country=pd.read_csv(r"C:\Users\nisha\Documents\python\python_projects\covid_19_analysis\covid-19_analysis_final\owid-covid-data.csv")
# df_for_all_country['date']= pd.to_datetime(df_for_all_country['date'])
df_for_all_country.head(300)


# In[50]:


df_afghanistan=df_for_all_country 

df_afghanistan.tail(300)


# In[51]:


mask = (df_afghanistan['date'] >= start_date) & (df_afghanistan['date'] <= end_date) & (df_afghanistan['location']=='Afghanistan')
df_afghanistan=df_afghanistan.loc[mask]
#retrieving the values from df_for_all_country with location afghanistan
df_afghanistan.head()


# In[52]:


df_afghanistan.tail()


# In[53]:



df_india=df_for_all_country
mask = (df_india['date'] >= start_date) & (df_india['date'] <= end_date) & (df_india['location']=='India')
df_india = df_india.loc[mask]
df_india.head()


# In[54]:


df_india.tail()


# In[55]:


df_china=df_for_all_country
mask = (df_china['date'] >= start_date) & (df_china['date'] <= end_date) & (df_china['location']=='China')
df_china = df_china.loc[mask]
df_china.head()


# In[56]:


df_china.tail()


# In[82]:


df_for_all_country['location'].unique() #get unique values of location column


# In[58]:


#plotting graph for total_cases of india using matplotlib
fig=plt.figure(figsize=(10,5),dpi=200)#setting the size of the figure
axes=fig.add_axes([0,0,1,1])
axes.bar(df_india['date'],df_india['total_cases'],color='orange')
axes.set_xlabel('Date')
axes.set_ylabel('Total cases')
axes.set_title('Total Confirmed Cases In India from jan 2021 to june 2021')


# In[59]:


#plotly express
fig1=px.bar(df_india,x='date',y='total_cases',color='total_cases',
            title='Total Cases In India From Jan 2021 To June 2021  ')
#use color as total_cases to get variation of colors according to value
fig1.show()


# In[60]:


#plotly express
fig1=px.bar(df_usa,x='date',y='us_total_cases',color='us_total_cases',
            title='Total Cases In USA From Jan 2021 To June 2021')
fig1.show()


# In[61]:


fig1=px.bar(df_singapore,x='date',y='cumulative_confirmed',color='cumulative_confirmed',
            title='Total Cases In Singapore From Jan 2021 To June 2021')
fig1.show()


# In[62]:


fig1=px.bar(df_afghanistan,x='date',y='total_cases',color='total_cases',
            title='Total Cases In Afghanistan Fom Jan 2021 To June 2021')
fig1.show()


# In[63]:


fig1=px.bar(df_china,x='date',y='total_cases',color='total_cases',
            title='Total Cases In China From Jan 2021 To June 2021')
fig1.show()


# In[64]:


df_india.iplot(kind='scatter',x='date',y='total_cases',mode='lines+markers',color='green',
               title='Total Cases In India From Jan 2021 To June 2021 ',
xTitle='Date',yTitle='Total Cases')


# In[65]:


df_china.iplot(kind='scatter',x='date',y='total_cases',mode='lines+markers',color='red',
               title='Total Cases In China From Jan 2021 To June 2021 ',
xTitle='Date',yTitle='Total Cases')


# In[66]:


df_afghanistan.iplot(kind='scatter',x='date',y='total_cases',mode='lines+markers',color='blue',
               title='Total Cases In Afghanistan From Jan 2021 To June 2021 ',
xTitle='Date',yTitle='Total Cases')


# In[67]:


df_singapore.iplot(kind='scatter',x='date',y='cumulative_confirmed',mode='lines+markers',
                   color='orange',
               title='Total Cases In Singapore From Jan 2021 To June 2021 ',
xTitle='Date',yTitle='Total Cases')


# In[68]:


df_usa.iplot(kind='scatter',x='date',y='us_total_cases',mode='lines+markers',
                   color='violet',
               title='Total Cases In USA From Jan 2021 To June 2021 ',
xTitle='Date',yTitle='Total Cases')


# In[ ]:





# In[ ]:





# In[69]:


#subplots

fig=make_subplots(rows=2,cols=2,specs=[[{"secondary_y":True},{"secondary_y":True}],
                                       [{"secondary_y":True},{"secondary_y":True}]],
                  subplot_titles=("India","China","Usa","Singapore"))

fig.add_trace(go.Bar(x=df_india['date'],y=df_india['total_cases'],
                     marker=dict(color=df_india['total_cases'],coloraxis="coloraxis")),1,1)

fig.add_trace(go.Bar(x=df_china['date'],y=df_china['total_cases'],
                     marker=dict(color=df_china['total_cases'],coloraxis="coloraxis")),1,2)

fig.add_trace(go.Bar(x=df_usa['date'],y=df_usa['us_total_cases'],
                     marker=dict(color=df_usa['us_total_cases'],coloraxis="coloraxis")),2,1)

fig.add_trace(go.Bar(x=df_singapore['date'],y=df_singapore['cumulative_confirmed'],
                     marker=dict(color=df_singapore['cumulative_confirmed'],
                                 coloraxis="coloraxis")),2,2)

fig.update_layout(coloraxis=dict(colorscale='Bluered_r'),showlegend=False,
                 title_text="Total Cases In 4 Countries",plot_bgcolor='rgb(230,230,230)')


# In[70]:


#subplots

fig=make_subplots(rows=2,cols=2,specs=[[{"secondary_y":True},{"secondary_y":True}],
                                       [{"secondary_y":True},{"secondary_y":True}]],
                  subplot_titles=("India","China","Usa","Singapore"))
fig.add_trace(go.Scatter(x=df_india['date'],y=df_india['total_cases'],
                     marker=dict(color=df_india['total_cases'])),1,1)

fig.add_trace(go.Scatter(x=df_china['date'],y=df_china['total_cases'],
                     marker=dict(color=df_china['total_cases'])),1,2)

fig.add_trace(go.Scatter(x=df_usa['date'],y=df_usa['us_total_cases'],
                     marker=dict(color=df_usa['us_total_cases'])),2,1)

fig.add_trace(go.Scatter(x=df_singapore['date'],y=df_singapore['cumulative_confirmed'],
                     marker=dict(color=df_singapore['cumulative_confirmed'])),2,2)

fig.update_layout(showlegend=False,
                 title_text="Total Cases In 4 Countries",plot_bgcolor='rgb(230,230,230)')


# In[84]:


df_for_all_country.fillna(0,inplace=True)#filling nan values with 0
df_for_all_country.head()


# In[72]:


df_for_all_country.query('location=="India"')#query to get rows where location =india


# In[73]:


df_for_all_country.groupby('date').sum().style.background_gradient(cmap='YlOrRd')


# In[74]:


total=df_for_all_country.groupby('date')['new_cases'].sum().sort_values(ascending=False).to_frame()
total


# In[75]:


total.style.background_gradient(cmap='YlOrRd')


# In[76]:


df_for_all_country.info() #getting the info of dataframe


# In[77]:


#grouping by date for all country

confirmed=df_for_all_country.groupby('date').sum()['total_cases'].reset_index()
total_deaths=df_for_all_country.groupby('date').sum()['total_deaths'].reset_index()
icu_patients =df_for_all_country.groupby('date').sum()['icu_patients'].reset_index()
hosp_patients=df_for_all_country.groupby('date').sum()['hosp_patients'].reset_index()
people_fully_vaccinated=df_for_all_country.groupby('date').sum()['people_fully_vaccinated'].reset_index()
new_cases=df_for_all_country.groupby('date').sum()['new_cases'].reset_index()
confirmed


# In[78]:


fig = make_subplots()
fig.add_trace(go.Scatter(x=confirmed['date'],y=confirmed['total_cases'],mode="lines",
                        name="total cases",line=dict(color="red",width=4)))

fig.add_trace(go.Scatter(x=total_deaths['date'],y=total_deaths['total_deaths'],mode="lines",
                        name="total deaths",line=dict(color="blue",width=4)))




fig.add_trace(go.Scatter(x=people_fully_vaccinated['date'],
                         y=people_fully_vaccinated['people_fully_vaccinated'],
                         mode="lines+markers",
                        name="people fully vaccinated",line=dict(color="green",width=2)))


# In[ ]:





# In[79]:


df_for_all_country.columns


# In[80]:


confirmed=df_for_all_country.groupby('date').sum()['total_cases'].reset_index()
total_deaths=df_for_all_country.groupby('date').sum()['total_deaths'].reset_index()
icu_patients =df_for_all_country.groupby('date').sum()['icu_patients'].reset_index()
hosp_patients=df_for_all_country.groupby('date').sum()['hosp_patients'].reset_index()
people_fully_vaccinated=df_for_all_country.groupby('date').sum()['people_fully_vaccinated'].reset_index()
new_cases=df_for_all_country.groupby('date').sum()['new_cases'].reset_index()
total_tests=df_for_all_country.groupby('date').sum()['total_tests'].reset_index()
population=df_for_all_country.groupby('date').sum()['population'].reset_index()
confirmed


# In[81]:


#summation for pie chart plotting
confirmed1=confirmed['total_cases'].sum()
total_deaths1=total_deaths['total_deaths'].sum()
icu_patients1=icu_patients['icu_patients'].sum()
hosp_patients1=hosp_patients['hosp_patients'].sum()
people_fully_vaccinated1=people_fully_vaccinated['people_fully_vaccinated'].sum()
total_tests1=total_tests['total_tests'].sum()
population1=population['population'].sum()




# In[82]:


labels = ['Confirmed Cases','Total Deaths','ICU Patients','Hospital Patients',
         'People Fully Vaccinated','Total Tests'] #labels of the pie chart
values = [confirmed1,total_deaths1,icu_patients1,hosp_patients1,
         people_fully_vaccinated1,total_tests1]#values of the pie chart

# Use `hole` to create a donut-like pie chart
fig = go.Figure(data=[go.Pie(labels=labels, values=values)])
fig.update_layout(title='Covid-19 Stat All Over The World')
fig.show()


# In[83]:


x_label=['population','People Fully Vaccinated','Confirmed Cases']
y_label=[population1,people_fully_vaccinated1,confirmed1]
fig = go.Figure([go.Bar(x=x_label, y=y_label)])
fig.update_layout(title='People Fully Vaccinated All Over The World With Respect To Population')
fig.show()


# In[84]:


# fig = make_subplots(specs=[[{"secondary_y": True}]])
# fig.add_trace(go.Scatter(x=confirmed['date'],y=confirmed['total_cases'],mode="lines",
#                         name="total cases(yaxis-1)",line=dict(color="red",width=4)),secondary_y=False)

# fig.add_trace(go.Scatter(x=total_deaths['date'],y=total_deaths['total_deaths'],mode="lines",
#                         name="total deaths(yaxis-2)",line=dict(color="blue",width=4)),secondary_y=True)


# fig.add_trace(go.Scatter(x=hosp_patients['date'],y=hosp_patients['hosp_patients'],
#                          mode="lines",
#                         name="hospital patients(yaxis-2)",line=dict(color="brown",width=4)),secondary_y=True)

# fig.add_trace(go.Scatter(x=people_fully_vaccinated['date'],
#                          y=people_fully_vaccinated['people_fully_vaccinated'],
#                          mode="lines+markers",
#                         name="people fully vaccinated",line=dict(color="green",width=2)))

# fig.add_trace(go.Scatter(x=new_cases['date'],y=new_cases['new_cases'],mode="lines",
#                         name="new cases(yaxis-1)",line=dict(color="purple",width=4)),secondary_y=False)


# In[ ]:





# In[85]:


#race bar graph plot


# In[86]:


#reading the csv file time_series_covid19_confirmed_global.csv

df_confirmed_worldwide=pd.read_csv(r'C:\Users\nisha\Documents\python\python_projects\covid_19_analysis\covid-19_analysis_final\time_series_covid19_confirmed_global.csv')
df_confirmed_worldwide.head()


# In[87]:


df_race_bar_chart=df_confirmed_worldwide 
#assigning the dataframe to another variable so that original dataframe  is not affected
df_race_bar_chart.drop(columns=['Province/State','Lat','Long'],inplace=True,axis=1)
#removing unnecessary columns


# In[88]:



df_race_bar_chart.head()


# In[89]:



df_race_bar_chart1=df_race_bar_chart.T#transposing the dataset 
new_header=df_race_bar_chart1.iloc[0] #assigning columns to a variable
df_race_bar_chart1=df_race_bar_chart1[1:] #retrieving rows starting from 1 index
df_race_bar_chart1.columns=new_header #assigning new columns to the dataframe
df_race_bar_chart1.head()


# In[90]:


df_race_bar_chart1= df_race_bar_chart1.loc[:,~ df_race_bar_chart1.columns.duplicated()]
#deleleting the duplicate columns
df_race_bar_chart1.info #to see all the information of dataframe
 


# In[91]:


#  now creating dataframes for each column that we want in our race bar graph because it is not 
# possible to plot all the columns thats why select specific columns
# make sure to convert the column to int because it would give error if we plot graph of type object

Afghanistan=df_race_bar_chart1['Afghanistan'].reset_index(drop=True).astype(str).astype(int)
Bangladesh=df_race_bar_chart1['Bangladesh'].reset_index(drop=True).astype(str).astype(int)
Belgium=df_race_bar_chart1['Belgium'].reset_index(drop=True).astype(str).astype(int)
Bhutan=df_race_bar_chart1['Bhutan'].reset_index(drop=True).astype(str).astype(int)
Brazil=df_race_bar_chart1['Brazil'].reset_index(drop=True).astype(str).astype(int)
China=df_race_bar_chart1['China'].reset_index(drop=True).astype(str).astype(int)
Canada=df_race_bar_chart1['Canada'].reset_index(drop=True).astype(str).astype(int)
France=df_race_bar_chart1['France'].reset_index(drop=True).astype(str).astype(int)
Germany=df_race_bar_chart1['Germany'].reset_index(drop=True).astype(str).astype(int)
India=df_race_bar_chart1['India'].reset_index(drop=True).astype(str).astype(int)
Iraq=df_race_bar_chart1['Iraq'].reset_index(drop=True).astype(str).astype(int)
Malaysia=df_race_bar_chart1['Malaysia'].reset_index(drop=True).astype(str).astype(int)
Mexico=df_race_bar_chart1['Mexico'].reset_index(drop=True).astype(str).astype(int)
Pakistan=df_race_bar_chart1['Pakistan'].reset_index(drop=True).astype(str).astype(int)
Russia=df_race_bar_chart1['Russia'].reset_index(drop=True).astype(str).astype(int)
Sri_Lanka=df_race_bar_chart1['Sri Lanka'].reset_index(drop=True).astype(str).astype(int)
Switzerland=df_race_bar_chart1['Switzerland'].reset_index(drop=True).astype(str).astype(int)
Turkey=df_race_bar_chart1['Turkey'].reset_index(drop=True).astype(str).astype(int)
US=df_race_bar_chart1['US'].reset_index(drop=True).astype(str).astype(int)
United_Kingdom=df_race_bar_chart1['United Kingdom'].reset_index(drop=True).astype(str).astype(int)


# In[92]:


#assigning date which is index of the df_race_bar_chart1 to date list
date=[]
for d in df_race_bar_chart1.index:
    date.append(d)
date


# In[93]:


# make sure to convert the date into series before using it in a dataframe
DATE = pd.Series(date)
DATE


# In[94]:


data = {'Afghanistan':Afghanistan,
'Bangladesh':Bangladesh,
'Belgium':Belgium,
'Bhutan':Bhutan,
'Brazil':Brazil,
'China':China,
'Canada':Canada,
'France':France,
'Germany':Germany,
'India':India,
'Iraq':Iraq,
'Malaysia':Malaysia,
'Mexico':Mexico,
'Pakistan':Pakistan,
'Russia':Russia,
'Sri Lanka':Sri_Lanka,
'Switzerland':Switzerland,
'Turkey':Turkey,
'US':US,
'United Kingdom':United_Kingdom,
        'Date' : DATE
       } #creating dictionary of columns that we want in our graph
race_bar_graph = pd.concat(data,axis = 1) 
race_bar_graph.set_index("Date", inplace = True) #assign index of the dataframe to date
race_bar_graph.head()


# In[95]:


race_bar_graph.index = pd.to_datetime(race_bar_graph.index) #converting index to datetime
race_bar_graph


# In[96]:


# at this stage all the steps of data cleaning and processing has been done now save the cleaned
# file in csv format
race_bar_graph.to_csv("corona_dataset_for_race_bar_graph.csv",header=True,index=True)
race_bar_graph.isnull().sum()


# In[97]:


race_bar_graph.info()


# In[98]:


import bar_chart_race as bcr


bcr.bar_chart_race(df=race_bar_graph,filename = None,
                   title= "Covid Cases Country-wise From Jan 2020 to July 2021")


# make sure to install ffmpeg before running bar_chart_race you can refer this link for downloading
# "https://www.wikihow.com/Install-FFmpeg-on-Windows". after installation make sure to install
# ffmpeg-python using cmd or anaconda prompt
# for cmd use "pip install ffmpeg-python"
# for anaconda prompt use "conda install ffmpeg-python"


# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:




