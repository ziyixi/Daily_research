#!/usr/bin/env python
############################################
# randomly select events for a given catalog
#
# usage:
# python catalog_selector.py catalog number
############################################

import sys

import numpy as np
import pandas as pd
from sklearn.cluster import KMeans


def sind(x):
    """sin(x) for x is in degree"""
    return np.sin(np.deg2rad(x))


def cosd(x):
    """cos(x) for x is in degree"""
    return np.cos(np.deg2rad(x))


def find_nearest(kmeans, data, label):
    """find the nearest event from the center if given a label

    Args:
        kmeans: the kmeans selector after fitting,
        data: the even catalog read by pandas,
        label: the group number

    Returns:
        event: the selected event represented by pandas row
    """
    temp = data[data.label == label]  # events with the label
    xmean = kmeans.cluster_centers_[label, 0]
    ymean = kmeans.cluster_centers_[label, 1]
    zmean = kmeans.cluster_centers_[label, 2]  # the center of each group
    dist = (temp.x-xmean)**2+(temp.y-ymean)**2+(temp.z-zmean)**2
    distp = dist.values
    po = distp.argmin()  # the position of the min distance in temp

    # return the index in all catalog
    return temp[po:po+1].index[0]


def main():
    """The main k-means part

    Args:
        None

    Returns:
        newdata: Selected catalog in pandas Dataframe
    """
    data = pd.read_table(sys.argv[1], delimiter="\s+",
                         usecols=(2, 3, 4), names=["latitude", "longitude", "depth"])
    data = data[data.depth < int(sys.argv[3])]  # depth restriction

    # reorder catalog after selected <300km
    data = pd.DataFrame(data.values, columns=[
                        "latitude", "longitude", "depth"])
    lat = data.latitude.values
    lon = data.longitude.values
    depth = data.depth.values

    newcoor = np.zeros(data.shape)
    R = 6371
    newcoor[:, 0] = (R-depth)*cosd(lat)*cosd(lon)
    newcoor[:, 1] = (R-depth)*cosd(lat)*sind(lon)
    newcoor[:, 2] = (R-depth)*sind(lat)  # x,y,z of each event

    kmeans = KMeans(n_clusters=N, random_state=6, n_jobs=-1).fit(newcoor)
    # 600 groups, random_state: random seed, njobs=-1: use all cores to calculate

    data["label"] = kmeans.labels_  # set the label for each event
    data["x"] = newcoor[:, 0]
    data["y"] = newcoor[:, 1]
    data["z"] = newcoor[:, 2]  # x,y,z for each event

    result = np.zeros(N, dtype=np.object)  # store selected events
    for i in range(N):
        temp = find_nearest(kmeans, data, i)
        result[i] = temp

    writedata = pd.read_table(sys.argv[1], delimiter="\s+", names=[
                              "date", "time", "latitude", "longitude", "depth", "Mw", "str"])
    writedata = writedata[writedata.depth < int(sys.argv[3])]
    writedata = pd.DataFrame(writedata.values, columns=[
                             "date", "time", "latitude", "longitude", "depth", "Mw", "str"])
    return writedata.iloc[result]


if(__name__ == "__main__"):
    N = int(sys.argv[2])
    newdata = main()
    with open(sys.argv[1]+".selected", "w") as f:
        for value in newdata.values:
            for item in value:
                f.write(str(item)+" ")
            f.write("\n")
