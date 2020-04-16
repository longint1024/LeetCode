class Solution:
    def updateMatrix(self, matrix: List[List[int]]) -> List[List[int]]:
        m, n = len(matrix), len(matrix[0])
        map = [[10000000 for i in range(n)]for j in range(m)]
        for i in range(m):
            for j in range(n):
                if matrix[i][j]==0:
                    map[i][j] = 0
        count = 1
        def dis(x:int,y:int)->int:
            dx, dy = [-1,1,0,0], [0,0,1,-1]
            MIN = 10000001
            for i in range(4):
                xx, yy = x+dx[i], y+dy[i]
                if xx>=0 and xx<m and yy>=0 and yy<n:
                    if map[xx][yy] < MIN:
                        MIN = map[xx][yy]
            return MIN
        while count:
            count = 0
            for i in range(m):
                for j in range(n):
                    if map[i][j] == 0:
                        continue
                    d = dis(i,j)
                    if map[i][j]>1+d:
                        count += 1
                        map[i][j] = 1+d
        return map