import pandas as pd
import numpy as np
from datetime import datetime

try:
    df = pd.read_csv("../data/data.csv")

    #replace MAC address by device name
    df = df.replace({
        "98:22:EF:53:81:45": "Laptop",
        "A8:9C:ED:37:54:E3": "Phone"
    })

    df = df.drop(columns = ["#"])
    df["TIME"] = pd.to_datetime(df["TIME"], format="%d/%m/%Y %H:%M:%S")
    df["DATE"] = df["TIME"].dt.date
    df["ONLINE TIME"] = df["ONLINE TIME"].apply(lambda x : int(x[0:2]) + int(x[3:5])/60)
    df["DOWNLOAD"] = df["DOWNLOAD"].str.split(" ").str[0].astype(float) * df["DOWNLOAD"].str.split(" ").str[1].replace({"MB": 1,"GB": 1000})
    df["UPLOAD"] = df["UPLOAD"].str.split(" ").str[0].astype(float) * df["UPLOAD"].str.split(" ").str[1].replace({"MB": 1,"GB": 1000})
    df["SUM"] = df["DOWNLOAD"] + df["UPLOAD"]

    #write log
    with open("../.log", "a") as f:
        f.write(f"{datetime.now()}\tPreprocess\tTransform data successfully\n")

    min_valid_date = df["DATE"].min()
    max_valid_date = df["DATE"].max()

    #fill missing date
    df1 = pd.DataFrame({
        "DATE":  np.tile(pd.date_range(df["DATE"].min(), df["DATE"].min() + pd.Timedelta(days = 20), freq = "D").date, 2),
        "MAC": [df["MAC"].unique()[0] for i in range(21)] + [df["MAC"].unique()[1] for i in range(21)],
    })

    df = pd.concat([df, df1]).reset_index(drop = True)
    df = df.drop_duplicates(subset = ["SUM", "DATE", "MAC"]).reset_index(drop = True)

    #write log
    with open("../.log", "a") as f:
        f.write(f"{datetime.now()}\tPreprocess\tAdd missing dates successfully\n")

    df["SUM"] = df[df["DATE"].between(min_valid_date, max_valid_date)]["SUM"].fillna(0)

    df.to_csv("../data/cleaned_data.csv", index = False)

    #write log
    with open("../.log", "a") as f:
        f.write(f"{datetime.now()}\tPreprocess\tPreproccess data successfully\n")

except Exception as e:
    print(e)

    #write log
    with open("../.log", "a") as f:
        f.write(f"{datetime.now()}\tPreprocess\tFail\n")