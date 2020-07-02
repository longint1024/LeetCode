from queue import PriorityQueue

class Solution:
    def kthSmallest(self, matrix: List[List[int]], k: int) -> int:
        if k==1:
            return matrix[0][0]
        n = len(matrix)
        pq = PriorityQueue()
        exist = [[0 for i in range(n)]for j in range(n)]
        pq.put((matrix[0][0],0,0))
        exist[0][0] = 1
        def judge(x:int,y:int) -> bool:
            if x<0 or y<0 or x>=n or y>=n:
                return False
            return True
        while k:
            value, x, y = pq.get()
            k = k-1
            if k==0:
                return value
            if judge(x+1,y) and not exist[x+1][y]:
                pq.put((matrix[x+1][y],x+1,y))
                exist[x+1][y] = 1
            if judge(x,y+1) and not exist[x][y+1]:
                pq.put((matrix[x][y+1],x,y+1))
                exist[x][y+1] = 1