import uuid
from collections import defaultdict

class Graph:

    def __init__(self):

        # Default dictionary to store graph
        self.graph: defaultdict[uuid.UUID, list[uuid.UUID]] = defaultdict(list[uuid.UUID])

    def addEdge(self, tail_vertex_id: uuid.UUID, head_vertex_id: uuid.UUID):
        self.graph[tail_vertex_id].append(head_vertex_id)

    
    def DFSUtil(self, vertex: uuid.UUID, visited: set[uuid.UUID]):
        visited.add(vertex)
        """
        Depth first search graph traversal utility.
        Recursive method, with cyclical validation.
        """

        # Recur for all the vertices
        # adjacent to this vertex
        for neighbour in self.graph[vertex]:
            if neighbour not in visited:
                self.DFSUtil(neighbour, visited)

    
    def DFS(self, v: uuid.UUID):
        """
        Depth first search graph traversal.
        Uses a recursive method
        """

        # Create a set to store visited vertices
        visited: set[uuid.UUID] = set()

        # Call the recursive helper function
        self.DFSUtil(v, visited)
        return visited
    
    def detectCycleUtil(self, vertex: uuid.UUID, visited: set[uuid.UUID], recStack: set[uuid.UUID]) -> bool:
        """
        Utility function to detect cycles in a directed graph using DFS.
        """
        # Mark the current node as visited and add it to the recursion stack
        visited.add(vertex)
        recStack.add(vertex)

        # Recur for all the vertices adjacent to this vertex
        for neighbour in self.graph[vertex]:
            # If the neighbour is not visited, recurse on it
            if neighbour not in visited:
                if self.detectCycleUtil(neighbour, visited, recStack):
                    return True
            # If the neighbour is in the recursion stack, a cycle is detected
            elif neighbour in recStack:
                return True

        # Remove the vertex from the recursion stack
        recStack.remove(vertex)
        return False

    def detectCycle(self) -> bool:
        """
        Detects if the graph contains a cycle.
        """
        visited: set[uuid.UUID] = set()
        recStack: set[uuid.UUID] = set()

        # Check for cycles in each connected component
        # Create a copy of the keys to avoid "dictionary changed size during iteration"
        vertices = list(self.graph.keys())
        for vertex in vertices:
            if vertex not in visited:
                try:
                    if self.detectCycleUtil(vertex, visited, recStack):
                        return True
                except Exception as e:
                    raise e
        return False
