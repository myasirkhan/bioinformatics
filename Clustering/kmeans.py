import random, sys, numpy, pprint

# points generated:
points = [2, 3, 4, 5, 6, 7, 8, 9, 1, 2, 3, 4, 5, 6, 7, 8, 9, 1, 2, 3, 4, 5, 6, 7, 8, 9, 1]
# how many clusters to make
num_clusters = 3
# how many iteration should be ran before printing the final result
num_iter = 3
# dict to hold mid points of data
mid_points = {}
# dict to hold all the clusters and points inside them
clustered_data = {}


def get_nearest_cluster(c_mid_points={}, c_point=0):
    nearest_point = sys.maxint
    i_nearest_point = -1
    for mps in c_mid_points.keys():
        if nearest_point > abs(c_point - c_mid_points[mps]):
            nearest_point = abs(c_point - c_mid_points[mps])
            i_nearest_point = mps

    return i_nearest_point


def get_new_mid_points(c_cluster):
    return numpy.mean(c_cluster)


def make_clusters():
    curr_iter = 0
    # initialize random mid points
    for i in range(0, num_clusters):
        if i not in mid_points.keys():
            mid_points[i] = random.choice(points)

    while curr_iter < num_iter:
        # assign points to clusters
        clustered_data = {}
        for i in range(0, num_clusters):
            clustered_data[i] = []
        for point in points:
            near_cluster = get_nearest_cluster(mid_points, point)
            clustered_data[near_cluster].append(point)

        # calculate new midpoints
        for i in range(0, num_clusters):
            mids = get_new_mid_points(clustered_data[i])
            mid_points[i] = mids
        curr_iter += 1

    # printing data:
    for i in clustered_data.keys():
        pprint.pprint("Cluster {} have points: {}".format(i, clustered_data[i]))

make_clusters()