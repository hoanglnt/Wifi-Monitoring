import pandas as pd
import numpy as np
import plotly.express as px
import plotly.offline as pyo
from plotly.subplots import make_subplots
from datetime import datetime

try:
    df = pd.read_csv("../data/cleaned_data.csv")

    #Figure 1
    data = df.groupby(["DATE", "MAC"]).agg({"ONLINE TIME": "sum", "SUM": "sum", "UPLOAD": "sum"}).reset_index()
    fig1 = px.bar(
        data, x = "DATE", y = "SUM", color = "MAC", barmode = "stack", title = "Dung lượng theo ngày",
        labels = {"DATE": "Ngày", "SUM": "MB"}
    )

    #write log
    with open("../.log", "a") as f:
        f.write(f"{datetime.now()}\tVisualize\tVizualize Figure 1 successfully\n")

    #Figure 2
    data = df.groupby("DATE")[["SUM"]].sum(min_count=1).sort_index(ascending = True).cumsum(skipna = False).reset_index()

    fig2 = px.line(
        data, x = "DATE", y = "SUM",
        color_discrete_sequence = ["green"], title = "Tổng dung lượng qua ngày",
        labels = {"DATE": "Ngày", "SUM": "MB"}
    )

    fig2.add_scatter(
        x = [data["DATE"].min(), data["DATE"].max()], y = [3000, 60000], 
        name = "Limit", mode = "lines", showlegend = False, line = {"color": "lightgray"}
    )

    #write log
    with open("../.log", "a") as f:
        f.write(f"{datetime.now()}\tVisualize\tVizualize Figure 2 successfully\n")

    #Figure 3
    data = [min(round(df["SUM"].sum() / 1000, 2), 60)]
    if data[0] < 60:
        data.append(60 - data[0])

    fig3 = px.pie(
        values = data,
    )

    fig3.update_traces(
        textinfo='value', 
        marker = dict(colors = ["green", "lightgray"]),
    )

    #write log
    with open("../.log", "a") as f:
        f.write(f"{datetime.now()}\tVisualize\tVizualize Figure 3 successfully\n")

    #combine and export html
    combine_fig = make_subplots(
        rows = 2, cols = 3, shared_xaxes = "all",
        specs = [[{"colspan" : 2}, {}, {}], [{"colspan" : 2}, {}, {"type": "domain"}]],
        column_widths=[0.5, 0.3, 0.2],
        subplot_titles = ("Dung lượng theo ngày", "", "", "Tổng dung lượng qua ngày")
    )

    combine_fig.add_trace(fig1['data'][0], row = 1, col = 1)
    combine_fig.add_trace(fig1['data'][1], row = 1, col = 1)
    combine_fig.add_trace(fig2['data'][0], row = 2, col = 1)
    combine_fig.add_trace(fig2['data'][1], row = 2, col = 1)
    combine_fig.add_trace(fig3['data'][0], row = 2, col = 3)

    combine_fig.update_layout(barmode = "stack")

    #write log
    with open("../.log", "a") as f:
        f.write(f"{datetime.now()}\tVisualize\tCombine successfully\n")

    pyo.plot(combine_fig, filename = "../report.html", auto_open = False)

    #write log
    with open("../.log", "a") as f:
        f.write(f"{datetime.now()}\tVisualize\tExport successfully at report.html\n")

except Exception as e:

    print(e)

    #write log
    with open("../.log", "a") as f:
        f.write(f"{datetime.now()}\tVisualize\tVisualize data failed\n")