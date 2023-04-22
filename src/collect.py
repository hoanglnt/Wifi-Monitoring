import sys
import requests
import pandas as pd
from datetime import datetime

url = "https://ex.login.net.vn/check/"
code = sys.argv[1]

try:
    response = requests.get(url + code)
    if response.status_code == 200:
        #read html
        df = pd.read_html(url + code)[1]
        df.to_csv("../data/data.csv", index = False)

        #write log
        with open("../.log", "a") as f:
            f.write(f"{datetime.now()}\tCollect\tDownload data successfully\n")

    else:
        #write log
        with open("../.log", "a") as f:
            f.write(f"{datetime.now()}\tCollect\tDownload data failed\n")

except Exception as e:
    print(e)

    #write log
    with open("../.log", "a") as f:
        f.write(f"{datetime.now()}\tCollect\tDownload data failed\n")
