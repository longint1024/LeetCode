class Solution:
    def isBipartite(self, graph: List[List[int]]) -> bool:
        n = len(graph)
        arr = [-1 for i in range(n)]
        while 1:
            st = -1
            for i in range(n):
                if arr[i] == -1:
                    st = i
                    arr[i] = 1
                    break
            if st == -1:
                return True
            queue, front, rear = [st], -1, 0
            while front<rear:
                front += 1
                node, color = queue[front], not arr[queue[front]]
                for i in graph[node]:
                    if arr[i] == (not color):
                        return False
                    if arr[i] == -1:
                        queue.append(i)
                        rear += 1
                        arr[i] = color