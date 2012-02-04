import numpy as np
from numpy.testing import assert_array_almost_equal
from scipy.sparse.csgraph import \
    cs_graph_shortest_path, dijkstra, floyd_warshall, construct_dist_matrix


def floyd_warshall_slow(graph, directed=False):
    N = graph.shape[0]

    #set nonzero entries to infinity
    graph[np.where(graph == 0)] = np.inf

    #set diagonal to zero
    graph.flat[::N + 1] = 0

    if not directed:
        graph = np.minimum(graph, graph.T)

    for k in range(N):
        for i in range(N):
            for j in range(N):
                graph[i, j] = min(graph[i, j], graph[i, k] + graph[k, j])

    graph[np.where(np.isinf(graph))] = 0

    return graph


def generate_graph(N=20):
    #sparse grid of distances
    dist_matrix = np.random.random((N, N))

    #make symmetric: distances are not direction-dependent
    dist_matrix += dist_matrix.T

    #make graph sparse
    i = (np.random.randint(N, size=N * N / 2),
         np.random.randint(N, size=N * N / 2))
    dist_matrix[i] = 0

    #set diagonal to zero
    dist_matrix.flat[::N + 1] = 0

    return dist_matrix


def test_floyd_warshall():
    dist_matrix = generate_graph(20)

    for directed in (True, False):
        graph_FW = cs_graph_shortest_path(dist_matrix, 'FW', directed)
        graph_py = floyd_warshall_slow(dist_matrix.copy(), directed)

        assert_array_almost_equal(graph_FW, graph_py)


def test_dijkstra():
    dist_matrix = generate_graph(20)

    for directed in (True, False):
        graph_D = cs_graph_shortest_path(dist_matrix, 'D', directed)
        graph_py = floyd_warshall_slow(dist_matrix.copy(), directed)

        assert_array_almost_equal(graph_D, graph_py)


def test_dijkstra_ind():
    dist_matrix = generate_graph(20)

    indices = np.arange(5)

    for directed in (True, False):
        graph_D = dijkstra(dist_matrix, directed, indices=indices)
        graph_FW = cs_graph_shortest_path(dist_matrix, 'FW', directed)

        print graph_D
        print graph_FW[:5]

        assert_array_almost_equal(graph_D, graph_FW[:5])


def test_predecessors():
    csgraph = generate_graph(20)

    for directed in (True, False):
        dist_D, pred_D = cs_graph_shortest_path(csgraph, 'D', directed,
                                                return_predecessors=True)
        dist_FW, pred_FW = cs_graph_shortest_path(csgraph, 'FW', directed,
                                                  return_predecessors=True)

        assert_array_almost_equal(dist_D, dist_FW)
        assert_array_almost_equal(pred_D, pred_FW)


def test_construct_shortest_path():
    csgraph = generate_graph(5)

    for directed in (True, False):
        dist, pred = cs_graph_shortest_path(csgraph,
                                            directed=directed,
                                            overwrite=False,
                                            return_predecessors=True)
        dist2 = construct_dist_matrix(csgraph, pred, directed=directed)

        assert_array_almost_equal(dist, dist2)


if __name__ == '__main__':
    import nose
    nose.runmodule()
