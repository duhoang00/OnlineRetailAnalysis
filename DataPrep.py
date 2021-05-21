import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from datetime import datetime


def invoiceCodeComlumn(row):
    if 'C' in str(row['InvoiceNo']):
        val = 'C'
    elif 'A' in str(row['InvoiceNo']):
        val = 'A'
    else:
        val = 'N'
    return val


def invoiceNumberColumn(row):
    if len(str(row['InvoiceNo'])) == 7:
        val = str(row['InvoiceNo'])[1:]
    else:
        val = str(row['InvoiceNo'])
    return val


def dateColumn(row):
    return datetime.strptime(str(row['InvoiceDate'])[0:10], '%Y-%m-%d').date()


def yearColumn(row):
    return str(row['InvoiceDate'])[0:4]


def monthColumn(row):
    return str(row['InvoiceDate'])[5:7]


def dataFilter(df):
    # Valid Price
    valid_price = df.UnitPrice >= 0
    # Valid Description
    valid_desc = df.Description.notnull()
    # Valid CID
    valid_CID = df.CustomerID.notnull()
    # Invoice type-N (Normal)
    inv_N = df.InvoiceCode == "N"
    # Invoice type-C (Cancellation)
    inv_C = df.InvoiceCode == "C"
    # Invoice type-N (Amendment)
    inv_A = df.InvoiceCode == "A"
    # Quantity Negative
    q_neg = df.Quantity < 0
    # Quantity Positive
    q_pos = df.Quantity >= 0

    # Path1 - Filter population down to include all
    # valid Customer IDs with Valid Price and Description
    p1 = valid_price & valid_desc & valid_CID

    # Path2 - Filter population down to include all
    # Normal (type-N) transactions with Positive Quantities
    p2 = inv_N & q_pos

    # Path3 - Filter population down to include all
    # Cancel (type-C) or Adjust (type-A) transactions
    # with Negative Quanitities
    p3 = (inv_A | inv_C) & q_neg

    # Path to Leafs: Combine Paths 1, 2 and 3:
    # *************** CREATE A COPY ************
    validData = df.loc[p1 & (p2 | p3)].copy()

    return validData


def DataPrep(applyFilter):
    # Load data
    input_df = pd.read_excel('./OnlineRetailData.xlsx')
    df = pd.DataFrame(input_df)

    # Add Invoice Number column
    df['InoiceNumber'] = df.apply(invoiceNumberColumn, axis=1)
    # Add Invoice Code column
    df['InvoiceCode'] = df.apply(invoiceCodeComlumn, axis=1)

    # Add Date column
    df['Date'] = df.apply(dateColumn, axis=1)
    # Add Year column
    df['Year'] = df.apply(yearColumn, axis=1)
    # Add Month column
    df['Month'] = df.apply(monthColumn, axis=1)
    # Add YearMonth column
    df['YearMonth'] = df['Year'] + df['Month']

    # Add Revenue column
    df['Revenue'] = df['UnitPrice'].astype(float) * df['Quantity'].astype(float)
    

    # Filter for suitable data
    if applyFilter == True:
        df = dataFilter(df)

    # Change columns type
    df['Date'] = pd.to_datetime(df['Date'], utc=True)
    df['YearMonth'] = pd.to_numeric(df['YearMonth'], downcast='integer')

    # Set date column as Index - Did not work
    df.set_index('Date', inplace=True)

    return df
