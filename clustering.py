# K-Means Clustering
# Importing the libraries
import matplotlib.pyplot as plt
import numpy
import pandas
import sys

from mpl_toolkits.mplot3d import Axes3D
from sklearn import preprocessing
from sklearn.cluster import KMeans


rnd_seed = 42
input_file_name = "data.csv"
columns = [4, 5, 6]
nan_replace = [-1, -10, -1]
scale_factor = [1, 0.1, 10]
max_cluster_count = 10
cluster_count = 4


def cluster(dataset, cluster_count, rnd_seed):
	X = dataset
	kmeans = KMeans(n_clusters = cluster_count, init = 'k-means++', random_state = rnd_seed)
	y_kmeans = kmeans.fit_predict(X)  # cluster appartenance
	print("cluster appartenance:", y_kmeans)

	# Visualising the clusters
	ax = Axes3D(plt.figure())
	ax.scatter(X[y_kmeans == 0, 0], X[y_kmeans == 0, 1], X[y_kmeans == 0, 2], c="red")
	ax.scatter(X[y_kmeans == 1, 0], X[y_kmeans == 1, 1], X[y_kmeans == 1, 2], c="blue")
	ax.scatter(X[y_kmeans == 2, 0], X[y_kmeans == 2, 1], X[y_kmeans == 2, 2], c="green")
	ax.scatter(X[y_kmeans == 3, 0], X[y_kmeans == 3, 1], X[y_kmeans == 3, 2], c="magenta")
	# ax.scatter(kmeans.cluster_centers_[:, 0], kmeans.cluster_centers_[:, 1], kmeans.cluster_centers_[:, 2], c="cyan")

	ax.set_xlabel('k stop')
	ax.set_ylabel('no w stop')
	ax.set_zlabel('is regular')
	plt.show()


def elbow(dataset, max_clusters, rnd_seed):
	wcss = []  # Within Cluster Sum of Squares
	for i in range(1, 1 + max_clusters):
		kmeans = KMeans(n_clusters = i, init = 'k-means++', random_state = rnd_seed)
		kmeans.fit(dataset)
		wcss.append(kmeans.inertia_)

	print("wcss =", wcss)
	plt.plot(range(1, 1 + max_clusters), wcss)
	plt.title('The Elbow Method')
	plt.xlabel('Number of clusters')
	plt.ylabel('WCSS')
	plt.show()
	return wcss


def extract_data(data_file_name, cols, nan_replace):
	dataset = pandas.read_csv(data_file_name, comment='#').iloc[:, 1:].values

	pos = dataset[dataset[:, 5] == 1]
	neg = dataset[dataset[:, 5] < 1]
	fpos = pos[pos[:, 6] == 0]
	fneg = neg[neg[:, 6] == 1]

	print(len(fpos)/len(pos))  # false positive rate
	print(len(fneg)/len(neg))  # false negative rate

	dataset = dataset[dataset[:, 5] < 1]	# delete regular claims
	dataset = dataset[dataset[:, 6] == 0]	# delete expected regulars
	dataset = dataset[:, cols]

	for i in range(len(cols)):
		dataset[numpy.isnan(dataset[:, i]), i] = nan_replace[i]
	return dataset


def feature_scaling(dataset, scalars):
	for i in range(len(scalars)):
		dataset[:, i] *= scalars[i]
	return dataset


if __name__ == "__main__":
	columns = [x - 1 for x in columns]  # ignore first column (language description)
	dataset = feature_scaling(extract_data(input_file_name, columns, nan_replace), scale_factor)
	print("dataset =", dataset)
	elbow(dataset, max_cluster_count, rnd_seed)
	cluster(dataset, cluster_count, rnd_seed)
