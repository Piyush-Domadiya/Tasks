#Dijkstra's Shortest Path Algorithm
import sys
import heapq

def dijkstra(graph, start):
    distances = {node: float('inf') for node in graph}
    distances[start] = 0
    queue = [(0, start)]

    while queue:
        current_distance, current_node = heapq.heappop(queue)

        if current_distance > distances[current_node]:
            continue

        for neighbor, weight in graph[current_node].items():
            distance = current_distance + weight

            if distance < distances[neighbor]:
                distances[neighbor] = distance
                heapq.heappush(queue, (distance, neighbor))

    return distances

# Example usage
graph = {
    'A': {'B': 1, 'C': 4},
    'B': {'C': 3, 'D': 2},
    'C': {'D': 1, 'E': 3},
    'D': {'A':2,'E':5},
    'E': {'C':2}
}

start_node = 'A'
shortest_distances = dijkstra(graph, start_node)


for node, distance in shortest_distances.items():
    print(f"Distance from {start_node} to {node} is {distance}")