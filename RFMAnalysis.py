import pandas as pd


def recencyDf(df):
    # Generate new dataframe based on unique CustomerID to keep track of RFM scores
    customer = pd.DataFrame(df['CustomerID'].unique())
    customer.columns = ['CustomerID']

    # Generate new data frame based on latest Invoice date from retail_ppp dataframe per Customer (groupby = CustomerID)
    recency = df.groupby('CustomerID').InvoiceDate.max().reset_index()
    recency.columns = ['CustomerID', 'LastPurchaseDate']

    # Set observation point as the last invoice date in the dataset
    LastInvoiceDate = recency['LastPurchaseDate'].max()

    # Generate Recency in days by subtracting the Last Purchase date for each customer from the Last Invoice Date
    recency['Recency'] = (
        LastInvoiceDate - recency['LastPurchaseDate']).dt.days

    # Consolidate to customer DataFrame
    customer = pd.merge(
        customer, recency[['CustomerID', 'Recency']], on='CustomerID')

    return customer


def frequencyDf(df):
    # Count number of invoices per CustomerID and store in new frequency Dataframe
    frequency = df.groupby(
        'CustomerID').InvoiceDate.count().reset_index()
    frequency.columns = ['CustomerID', 'Frequency']

    # Consolidate Frequency to existing Customer DataFrame

    customer = pd.merge(customer, frequency, on='CustomerID')

    return frequency
