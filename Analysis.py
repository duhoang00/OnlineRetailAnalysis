import pandas as pd
import seaborn as sns
import numpy as np
from Lib import print2Excel, analysisAnimation
from DataPrep import DataPrep
from KPIAnalysis import monthlyKPI, customerKPI
from RFMAnalysis import RFMAnalysis
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
from matplotlib import pyplot as plt
from KMeansLib import k_means
from KMeansLib import k_means


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

    Xstd['clusters'] = cluster_labels

    dataset = Xstd.values
    colors = np.array(['r', 'g', 'b'])

    cen, distances, cluster_assigning = k_means(dataset, k)

    plt.scatter(x = Xstd['Recency'], y = Xstd['Frequency'], c=colors[distances], s=2)
    plt.xlabel('Recency')
    plt.ylabel('Frequency')
    plt.savefig('fig_clus_Recency_Frequency.png', dpi=300, bbox_inches='tight')

    plt.scatter(x = Xstd['Recency'], y = Xstd['Revenue'], c=colors[distances], s=2)
    plt.xlabel('Recency')
    plt.ylabel('Revenue')
    plt.savefig('fig_clus_Recency_Revenue.png', dpi=300, bbox_inches='tight')

    plt.scatter(x = Xstd['Frequency'], y = Xstd['Revenue'], c=colors[distances], s=2)
    plt.xlabel('Frequency')
    plt.ylabel('Revenue')
    plt.savefig('fig_clus_Frequency_Revenue.png', dpi=300, bbox_inches='tight')


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
