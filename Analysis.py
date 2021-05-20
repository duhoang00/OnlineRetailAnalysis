import threading
import pandas as pd
from Lib import print2Excel, analysisAnimation
from DataPrep import DataPrep
from KPIAnalysis import monthlyKPI, customerKPI
from RFMAnalysis import recencyDf, frequencyDf


def Analysis():
    df = DataPrep(applyFilter=True)
    # print(df["YearMonth"]) # Work as expected

    mKPI = monthlyKPI(df)
    print(mKPI)

    newDf, cKPI = customerKPI(df)
    print(cKPI)


def process():
    Analysis()


process()
