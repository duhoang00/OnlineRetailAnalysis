import numpy as np
import pandas as pd
from matplotlib import pyplot as plt


def calc_dist_euclidean(vec_1, vec_2):

    distances = np.sqrt(((vec_1 - vec_2[:, np.newaxis]) ** 2).sum(axis=2))
    dist_euclidean = np.argmin(distances, axis=0)

    return dist_euclidean


def init_cent(dataset, k):

    centroids = dataset.copy()
    np.random.shuffle(centroids)

    return centroids[:k]

def k_means(dataset, k):

    centroids = init_cent(dataset, k)

    distances = calc_dist_euclidean(dataset, centroids)

    cluster_assigning = np.array([dataset[distances == k].mean(axis=0) for k in range(centroids.shape[0])])

    return centroids, distances, cluster_assigning