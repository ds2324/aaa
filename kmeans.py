import numpy as np
from numpy.linalg import norm
from pyspark import SparkConf, SparkContext


def assign_centroid(datapoint, initial_centroid):
    min_dist = np.inf
    which_centroid = 0
    for idx, c in enumerate(initial_centroid):
        dist = norm(datapoint - c)
        if dist < min_dist:
            min_dist = dist
            which_centroid = idx
    return which_centroid


def write_centroid(centroid):
    file = open("final_centroid.txt", "w")
    for c in centroid:
        line = ""
        for item in c:
            line += str(item) + " "
        file.write(line + "\n")
    file.close()


def pyspark_kmeans(data_txt, centroid_txt):

    max_iter = 100

    conf = SparkConf()
    sc = SparkContext(conf=conf)

    data = sc.textFile(data_txt).map(lambda line: np.array([float(x) for x in line.split(' ')])).cache()
    centroid = sc.textFile(centroid_txt).map(lambda line: np.array([float(x) for x in line.split(' ')])).collect()

    for i in range(max_iter):

        old_centroid = centroid
        # Assign clusters
        assigned_data = data.map(lambda l: (assign_centroid(l, old_centroid), l))

        # Compute clusters
        cluster_sum = assigned_data.mapValues(lambda l: (l, 1)).reduceByKey(lambda a, b: (a[0] + b[0], a[1] + b[1]))
        centroid = cluster_sum.map(lambda l: l[1][0] / l[1][1]).collect()

    write_centroid(centroid)


if __name__ == '__main__':
    pyspark_kmeans(data_txt='/Users/sunduo/Downloads/ORIE5270/data.txt', centroid_txt='/Users/sunduo/Downloads/ORIE5270/c1.txt')
