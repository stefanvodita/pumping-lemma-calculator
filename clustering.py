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
	dataset = pandas.read_csv(data_file_name, comment='#').iloc[:, cols].values
	# dataset[numpy.isnan(dataset)] = nan_replace
	for i in range(len(cols)):
		dataset[numpy.isnan(dataset[:, i]), i] = nan_replace[i]
	return dataset


def feature_scaling(dataset, scalars):
	# return preprocessing.scale(dataset)
	for i in range(len(scalars)):
		dataset[:, i] *= scalars[i]
	return dataset


if __name__ == "__main__":
	dataset = feature_scaling(extract_data("data.csv", [4, 5, 6], [-1, -10, -1]), [1, 1/10, 10])
	print("dataset =", dataset)
	elbow(dataset, 10, rnd_seed)
	cluster(dataset, 3, rnd_seed)
