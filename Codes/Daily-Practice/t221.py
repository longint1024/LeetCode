class Solution:
    def maximalSquare(self, matrix: List[List[str]]) -> int:
        if matrix == []:
            return 0
        m, n = len(matrix),len(matrix[0])
        MAX = 0
        map = [[int(matrix[i][j]) for j in range(n)]for i in range(m)]
        for i in range(m):
            if map[i][0]:
                MAX = 1
        for j in range(n):
            if map[0][j]:
                MAX = 1
        for i in range(1,m):
            for j in range(1,n):
                if map[i][j]:
                    map[i][j] = min(min(map[i][j-1],map[i-1][j]),map[i-1][j-1])+1
                if map[i][j]>MAX:
                    MAX = map[i][j]
        return MAX**2