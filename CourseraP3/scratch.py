# import collections
#
#
# def bfs(graph, start, end):
#     visited, queue = collections.defaultdict(list), collections.deque([start])
#     visited[start]
#     while queue:
#         vertex = queue.popleft()
#         for neighbour in graph[vertex]:
#             if neighbour == end:
#                 visited[neighbour].append(vertex)
#                 queue.clear()
#                 break
#
#             elif neighbour not in visited:
#                 visited[neighbour].append(vertex)
#                 queue.append(neighbour)
#
#     if len(graph) == len(visited):
#         return visited
#     return bfs(visited, end, start)
#
#
# if __name__ == '__main__':
#     graph = {
#         1: [2, 3, 4],
#         4: [7, 8],
#         3: [],
#         2: [5, 6],
#         8: [],
#         9: [],
#         10: [],
#         11: [],
#         12: [],
#         7: [11, 12],
#         5: [9, 10],
#         6: []
#     }
#     print(bfs(graph, 1, 5))


# import requests
#
# resp = requests.get('http://127.0.0.1:8000/template/echo/?a=1', headers={'X-Print-Statement': 'test'})
# print(resp.content)
