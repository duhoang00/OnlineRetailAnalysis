import threading
import numpy
import pandas as pd
from Lib import print2Excel, analysisAnimation
from DataPrep import DataPrep
from KPIAnalysis import monthlyKPI, customerKPI
from RFMAnalysis import RFMAnalysis
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
from sklearn import metrics
import matplotlib.pyplot as plt


def RFMScoreImage(customerRFM):
    fig_Recency_Frequency = customerRFM.plot.scatter(
        x='Recency', y='Frequency', c='DarkBlue').get_figure()
    fig_Recency_Frequency.savefig('fig_Recency_Frequency.png')

    fig_Recency_Revenue = customerRFM.plot.scatter(
        x='Recency', y='Revenue', c='DarkBlue').get_figure()
    fig_Recency_Revenue.savefig('fig_Recency_Revenue.png')

    fig_Frequency_Revenue = customerRFM.plot.scatter(
        x='Frequency', y='Revenue', c='DarkBlue').get_figure()
    fig_Frequency_Revenue.savefig('fig_Frequency_Revenue.png')


def KMeansCluster(df):
    # Number of clusters
    k = 3

    scaler = StandardScaler()
    Xstd = pd.DataFrame(scaler.fit_transform(df), columns=df.columns)

    model = KMeans(n_clusters=k, random_state=0)
    model.fit(Xstd)

    cluster_labels = model.labels_

    centroids = model.cluster_centers_

    Xstd['clusters'] = cluster_labels

    fig_clus_Recency_Frequency = Xstd.plot.scatter(
        x='Recency', y='Frequency').get_figure()
    fig_clus_Recency_Frequency.savefig('fig_clus_Recency_Frequency.png')

    


def Analysis():
    df = DataPrep(applyFilter=True)

    mKPI = monthlyKPI(df)

    newDf, cKPI = customerKPI(df)

    customerRFM = RFMAnalysis(newDf)

    # RFMScoreImage(customerRFM)

    KMeansCluster(customerRFM)


def process():
    Analysis()


process()
