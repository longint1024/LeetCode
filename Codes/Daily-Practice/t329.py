class Solution:
    def longestIncreasingPath(self, matrix: List[List[int]]) -> int:
        if matrix == []:
            return 0
        m, n = len(matrix), len(matrix[0])
        ans = [[1 for i in range(n)]for j in range(m)]
        dx, dy = [1,-1,0,0], [0,0,1,-1]
        MAX = 1
        def judge(x:int,y:int,i:int,j:int)->bool:
            if x<0 or x>m-1 or y<0 or y>n-1:
                return False
            if matrix[x][y]>=matrix[i][j]:
                return False
            if ans[x][y] < ans[i][j]:
                return False
            return True
        while 1:
            flag = 0
            for i in range(m):
                for j in range(n):
                    for k in range(4):
                        if judge(i+dx[k],j+dy[k],i,j):
                            ans[i][j] = ans[i+dx[k]][j+dy[k]] + 1
                            if ans[i][j]>MAX:
                                MAX = ans[i][j]
                            flag = 1
            if not flag:
                break
        return MAX