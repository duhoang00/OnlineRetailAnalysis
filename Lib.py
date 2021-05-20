import sys
import time
import threading
import pandas as pd


def print2Excel(df, fileName):
    writer = pd.ExcelWriter(fileName)
    df.to_excel(writer)
    writer.save()


def analysisAnimation():
    chars = "/—\|"
    for char in chars:
        sys.stdout.write('\r'+'Loading...'+char)
        time.sleep(.1)
        sys.stdout.flush()
