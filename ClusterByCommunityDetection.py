# coding=utf-8

import Levenshtein
import igraph

class ClusterByCommunityDetection:

    def __init__(self, clustering_objects):
        """
        :param clustering_objects: 聚类对象列表，数据类型为list
        """
        self.clustering_objects = clustering_objects
        self.similarity_matrix = self.get_similarity_matrix()
        self.clusters = self.clustering()

    def get_similarity_matrix(self):
        """
        function:构建相似度矩阵
        :return: similarity_matrix : 聚类对象相似度矩阵
        """
        nums = self.clustering_objects.__len__()  # 聚类对象的个数
        similarity_matrix = [[0 for col in range(nums)] for row in range(nums)]
        for i in range(0, nums, 1):
            object_i = self.clustering_objects[i]
            for j in range(0, nums, 1):
                object_j = self.clustering_objects[j]
                similarity = Levenshtein.ratio(object_i, object_j)
                if similarity > 0.5:
                    similarity_matrix[i][j] = similarity * 10
                    # similarity_matrix[j][i] = similarity * 10
                else:
                    similarity_matrix[i][j] = 0
                    # similarity_matrix[j][i] = 0
        return similarity_matrix

    def clustering(self):
        """
        function:使用了社会划分算法进行聚类
        :return: new_clusters :聚类对象大于２的所有簇
        """
        nodes = self.similarity_matrix.__len__()
        g = igraph.Graph(nodes)
        weights = []
        edges = []
        for i in range(0, nodes, 1):
            for j in range(0, nodes, 1):
                if self.similarity_matrix[i][j] > 0:
                    edges += [(i, j)]
                    weights.append(self.similarity_matrix[i][j])
        g.add_edges(edges)
        g = g.simplify()
        clusters = g.community_multilevel(weights)
        new_clusters = list()
        for one_cluster in clusters:
            if one_cluster.__len__() > 2:
                new_one_cluster = list()
                for i in one_cluster:
                    new_one_cluster.append(self.clustering_objects[i])
                new_clusters.append(new_one_cluster)
        return new_clusters

    def get_clusters(self):
        return self.clusters


def main():
    f = open('test.txt', 'r')
    cluster_data = f.readlines()
    for i in range(0, cluster_data.__len__(), 1):
        cluster_data[i] = cluster_data[i].replace('\n', '')
    clusters = ClusterByCommunityDetection(cluster_data).get_clusters()
    for one_cluster in clusters:
        print '-------------'
        for i in one_cluster:
            print i

if __name__ == '__main__':
    main()