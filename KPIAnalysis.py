import pandas as pd


def monthlyKPI(df):
    # year = pd.to_datetime(df['Date']).dt.year
    # month = pd.to_datetime(df['Date']).dt.month

    # 1. Revenue - Generate Monthly KPIs DataFrame by aggregating Revenue
    m_kpis = pd.DataFrame(df.groupby(
        [df.index.year, df.index.month])['Revenue'].sum())

    # 2. Generate Monthly Growth rate based on previous months revenue
    m_kpis['MonthlyGrowth'] = m_kpis['Revenue'].pct_change()

    # 3. Generate Active Customers
    m_kpis['ActiveCustomers'] = pd.DataFrame(df.groupby(
        [df.index.year, df.index.month])['CustomerID'].nunique())

    # 4. Generate Monthly Order Count (Quantity)
    m_kpis['MonthlyOrderCount'] = pd.DataFrame(df.groupby(
        [df.index.year, df.index.month])['Quantity'].sum())

    # 5. Gengerate Monthly Order Average
    m_kpis['MonthlyOrderAverage'] = pd.DataFrame(df.groupby(
        [df.index.year, df.index.month])['Revenue'].mean())

    # Rename index to capture Year and Month
    m_kpis.index.set_names(['Year', 'Month'], inplace=True)

    return m_kpis


def customerKPI(df):
    # Generate new dataframe based on CustomerID and its first purchase date
    customer_fist_purchase = df.groupby(
        'CustomerID').InvoiceDate.min().reset_index()
    customer_fist_purchase.columns = ['CustomerID', 'FirstPurchaseDate']
    customer_fist_purchase['FirstPurchaseYearMonth'] = customer_fist_purchase['FirstPurchaseDate'].map(
        lambda date: 100*date.year + date.month)

    # Add first purchase date column to the new Customer Dataframe by merging with the original retail_pp
    newDf = pd.merge(df, customer_fist_purchase, on='CustomerID')
    newDf['Date'] = pd.to_datetime(newDf.InvoiceDate.dt.date)
    newDf.set_index('Date', inplace=True)
    newDf.head()

    # Create new column "User Type" and default it to "New" as its values. Assign "Existing" value if
    # User's "FirstPurchaseYearMonth" was before the selected "InvoiceYearMonth"
    newDf['UserType'] = 'New'

    newDf.loc[newDf['YearMonth'] >
              newDf['FirstPurchaseYearMonth'], 'UserType'] = 'Existing'

    # Calculate the Revenue per month for each user type
    customer_kpis = pd.DataFrame(newDf.groupby(
        [newDf.index.year, newDf.index.month, newDf.UserType])['Revenue'].sum())
    customer_kpis.index.set_names(['Year', 'Month', 'UserType'], inplace=True)

    return newDf, customer_kpis
