### IMPORTANT VARIABLES
import os
PS = os.path.sep

db_file = "db" + PS + "product_price_monitor.db"


###CONNECTOR HELPER FUNCTIONS
import sqlite3
from sqlite3 import Error

def create_connection(db_file):
    """ create a database connection to the SQLite database
        specified by db_file
    :param db_file: database file
    :return: Connection object or None
    """
    con = None
    try:
        con = sqlite3.connect(db_file, timeout=5)
        return con
    except Error as e:
        print(e)

    return con

def close_connection(con):
    """ close database connection to the SQLit database after your doings
    :param con: Connection object
    :return:
    """
    try:
        con.close()
    except Error as e:
        print(e)


# create a database connection
def create_graphic():
    # create a database connection
    import sqlite3
    from sqlite3 import Error

    con = create_connection(db_file)
    cur = con.cursor()
    cur.execute("SELECT * FROM tbl")
    datasets = cur.fetchall()
    con = close_connection(con)

    print ('INFO: Datasets were read from DB', db_file, '..')
    #print(datasets)

    #create graphic-pngs
    import pandas as pd
    import numpy as np

    colors_list = ["tab:blue", "tab:orange", "tab:green", "tab:red"]

    #Tuning of Data (projection of relevant columns, Timestamp convertion)
    df = pd.DataFrame(datasets, columns=["RowID","Timestamp", "Product", "Model", "Price"])

    df["Date"] = pd.to_datetime(df['Timestamp'], unit='s').dt.date
    df.set_index('Date', inplace=True)


    #Matplotlib Configuration
    #Figure 1 - Daily
    import matplotlib as mpl
    import matplotlib.pyplot as plt

    plt.figure();
    plt.title("Product Price Monitor - Graphic Card Models (Daily)")
    plt.ylabel("Commodity Price [€]")

    #Generation of series plot lines
    model_list = df["Model"].unique().tolist()

    for i in range(len(model_list)):
        df[df["Model"] == model_list[i]].groupby(["Date"])['Price'].min().plot(linestyle='-', color=colors_list[i], legend = True, label=model_list[i]+" Min")
        df[df["Model"] == model_list[i]].groupby(["Date"])['Price'].median().plot(linestyle='--', color=colors_list[i], legend = True, label=model_list[i]+" Median")

    #Place the legend outside of the graph
    plt.legend(bbox_to_anchor=(1.03, 1.03), loc='upper left')

    plt.xticks(rotation=75)

    plt.savefig("img" + PS + "daily.png", bbox_inches = "tight")

    #---

    #Matplotlib Configuration
    #Figure 2 - Intraday
    import matplotlib as mpl
    import matplotlib.pyplot as plt

    plt.figure();
    plt.title("Product Price Monitor - Graphic Card Models (Daily)")
    plt.ylabel("Commodity Price [€]")

    #Generation of series plot lines
    model_list = df["Model"].unique().tolist()

    for i in range(len(model_list)):
        df[df["Model"] == model_list[i]].groupby(["Timestamp"])['Price'].min().plot(linestyle='-', color=colors_list[i], legend = True, label=model_list[i]+" Min")
        df[df["Model"] == model_list[i]].groupby(["Timestamp"])['Price'].median().plot(linestyle='--', color=colors_list[i], legend = True, label=model_list[i]+" Median")

    #Place the legend outside of the graph
    plt.legend(bbox_to_anchor=(1.03, 1.03), loc='upper left')

    plt.xticks(rotation=75)

    plt.savefig("img" + PS + "intraday.png", bbox_inches = "tight")

import time
while True:
    create_graphic()
    print ('INFO: Graphics written to disk..')
    print ('INFO: Next data collection will run in 3 hours..')
    time.sleep(60*60*3)
