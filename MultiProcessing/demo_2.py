import pandas as pd
import numpy as np
from fuzzywuzzy import fuzz
from fuzzywuzzy import process
import time
from multiprocessing import Pool
import csv


count = 0
my_file_name = "output.csv"


def mainFunction(index):
    global acq_data
    row = [acq_data.iloc[index, 0]] + [
        item[0].replace(",", " ").replace("|", " ")
        for item in process.extract(acq_data.iloc[index, 0], bank_data)
    ]
    # print("now {} rows left".format(acq_data["0"].isnull().sum()))
    with open(my_file_name, "a+", newline="") as f:
        ff = csv.writer(f)
        ff.writerow(row)


if __name__ == "__main__":
    start_time = time.time()
    with open(my_file_name, "w+", newline="") as f:
        ff = csv.writer(f)
        ff.writerow(["Acquirer", 0, 1, 2, 3, 4])

    acq_data = pd.read_excel("acquirers.xlsx", usecols=[2])
    acq_data = acq_data.reindex(columns=["Acquirer Name"] + list("01234"))

    bank_data = pd.read_csv("bank_names.csv").iloc[:, 1].tolist()

    start_time = time.time()

    p = Pool(processes=6)
    p.map(mainFunction, range(len(acq_data)))

    print("\nRun in --- %s seconds ---" % (time.time() - start_time))
    # acq_data.to_csv("myresult.csv")

