import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import requests 
from shiny import App, ui, render, reactive 

#loading my data into my shiny app
df = pd.read_csv("assessments/summative1/attendance_anonymised.csv")
df = df.drop(columns = "Planned End Date")
df.rename(columns = {
    'Unit Instance Code' : 'Module Code',
    'Calocc Code' : 'Year',
    'Long Description' : 'Module Name',
    'Register Event ID' : 'Event ID',
    'Register Event Slot ID' : 'Event Slot ID',
    'Planned Start Date' : 'Date',
    'is Positive' : 'Has Attended',
    'Postive Marks' : 'Attended',
    'Negative Marks' : 'NotAttended',
    'Usage Code' : 'Attendance Code'
    }, inplace = True)
df["Date"] = pd.to_datetime(df["Date"])

#UI
ui = ui.page_sidebar( #creating a page with a sidebar
    ui.sidebar(
        ui.input_select(
            "module_select", #input ID
            "Pick a Module", #title of the sidebar
            choices = sorted(df["Module Name"].unique()), selected = None), #setting the module options to choose from
        ),
    ui.h2("Average attendance rate over time for a chosen module"), #creating a title for the page
    ui.output_plot("plot") #placeholder for my plot
)

#SERVER
def server(input, output, session):
    @output
    @render.plot #creating a plot output
    def plot():
        selected_module = input.module_select() #accessing the selected module
        filter = df[df["Module Name"] == selected_module] #creating a filtered datadrame for each selected module
        att = filter.groupby("Date")["Attended"].mean().reset_index() #summarising attendance over time
             #by grouping each row by date, calculating average attendance for each date, and turning the series back into a dataframe

        fig, ax = plt.subplots(figsize = (12, 6)) #creating a matplotlib figure and axis to plot on
        ax.plot(att["Date"], att["Attended"]) #plotting the average attendance over time
        ax.set_title(f"Average attendance rate over time for {selected_module}") #plot labels
        ax.set_xlabel("Date")
        ax.set_ylabel("Attendance Rate")
        ax.grid(True)
        
        return fig #returning matplotlib figure object

#APP
app = App(ui, server)