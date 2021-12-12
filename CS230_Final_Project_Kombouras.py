"""
Name:       George Kombouras
CS230:      Section 4
Data:       Fortune 500 Companies
URL:        Link to your web application online (see extra credit)
Description:
The program uses the Fortune_500_Corporate_Headquarters.csv file to analyze company data from various states.
The project includes a dataset and map that is filtered by the rankings of the companies.
It also includes a bar chart that shows the number of employees per company in a certain state that is selected.
The second bar chart shows the count of Fortune 500 companies in the different states.
The color of the charts can be selected by the user.
The end includes a statistics section for the companies in the states that are selected.
"""

from pandas import DataFrame, read_csv
import os
import streamlit as st
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import sys
import matplotlib
import dateutil
import pydeck as pdk


# Read in data
def read_file(datafile="Fortune_500_Corporate_Headquarters.csv"):
    df = pd.read_csv(datafile)
    df["EMPLOYEES"] = df["EMPLOYEES"].astype(float)
    return df


# Function for first bar chart
def bar_chart1(selectedstatedata, state, color):
    plt.figure()
    plt.title(f"Number of Employees of Fortune 500 Companies in {state}")
    plt.ylabel("Employees", fontsize=16, fontweight="bold")
    plt.xlabel("Company Name", fontsize=16, fontweight="bold")
    plt.xticks(rotation='vertical')
    plt.bar(selectedstatedata["NAME"], selectedstatedata["EMPLOYEES"], color=color, edgecolor="black")
    return plt


# Function for second chart
def bar_chart2(fd, color2):
    plt.figure()
    plt.title(f"Number of Fortune 500 Companies (Per State)")
    plt.ylabel("Number of Fortune 500 Companies", fontsize=16, fontweight="bold")
    plt.xlabel("State Name", fontsize=16, fontweight="bold")
    plt.xticks(rotation='vertical')
    plt.bar(fd["STATE"], fd["Counts"], color=color2, edgecolor="black")
    return plt


# Frequency Function for States
def freq_data(df, states):
    freq_dict = {}
    for state in states:
        freq = 0
        for i in range(len(df)):
            if df[i][5] == state:
                freq += 1
        freq_dict[state] = freq
    return freq_dict


def main():
    # Page Formatting
    st.header("Fortune 500 Companies Analysis")
    st.sidebar.header("Company Filters")
    df = read_file()

    # Employees Slider for Dataset
    ranks = df["RANK"]
    print(ranks)
    min_slider = int(df['RANK'].min())
    max_slider = int(df['RANK'].max())
    max_ranks = st.sidebar.slider("Slide for Ranking", min_value=min_slider, max_value=max_slider)

    # Map Creation
    df_filtered = df[df['RANK'] <= max_ranks]
    st.write("Data Set Based Upon Ranking Filter:")
    st.write(df_filtered)
    df_filtered["lon"] = df_filtered["LONGITUDE"]
    df_filtered["lat"] = df_filtered["LATITUDE"]
    map_data = df_filtered[["lon", "lat"]]
    st.map(map_data)

    # State Selection Drop Down Box (For Bar Chart)
    states = df['STATE'].unique()
    state = st.sidebar.selectbox('State (For Bar Charts)', states)
    selectedstatedata = df[df['STATE'] == state]
    color = st.sidebar.color_picker('Pick A Color (For Bar Charts)', '#7AD8D8')
    st.sidebar.write('The current selected color is', color)
    st.pyplot(bar_chart1(selectedstatedata=selectedstatedata, state=state, color=color))
    st.set_option('deprecation.showPyplotGlobalUse', False)

    # Country Selection (For Statistics)
    states2 = df['STATE'].unique()
    state2 = st.sidebar.multiselect('States Selection (For Statistics)', states2)
    fd = df['STATE'].value_counts().rename_axis("STATE").reset_index(name="Counts")
    print(fd)
    selectedstatedata2 = df['STATE'].isin(state2)
    selectedstatedata2 = df[selectedstatedata2]
    selectedstatedata2_count = selectedstatedata2["STATE"].count()

    # Bar Chart2 Creation
    st.pyplot(bar_chart2(fd=fd, color2=color))

    # Selected States Statistics
    st.write("Statistics and Data for Selected States:")
    st.write(selectedstatedata2)
    st.write("Number of Fortune 500 Companies in Selected States:", selectedstatedata2_count)
    rank_mean = selectedstatedata2["RANK"].mean()
    st.write("Average Rank: ", rank_mean)
    rank_max = selectedstatedata2["RANK"].max()
    rank_min = selectedstatedata2["RANK"].min()
    st.write("Maximum Rank: ", rank_max)
    st.write("Minimum Rank: ", rank_min)
    revenues_mean = selectedstatedata2["REVENUES"].mean()
    st.write("Average Revenue: ", revenues_mean)
    employees_mean = selectedstatedata2["EMPLOYEES"].mean()
    employees_max = selectedstatedata2["EMPLOYEES"].max()
    employees_min = selectedstatedata2["EMPLOYEES"].min()
    st.write("Average Number of Employees: ", employees_mean)
    st.write("Maximum Number of Employees: ", employees_max)
    st.write("Minimum Number of Employees: ", employees_min)


main()
