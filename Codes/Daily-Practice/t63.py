class Solution:
    def uniquePathsWithObstacles(self, obstacleGrid: List[List[int]]) -> int:
        m = len(obstacleGrid)
        n = len(obstacleGrid[0])
        ans = [0 for i in range(n)]
        if obstacleGrid[0][0]:
            return 0
        else:
            ans[0] = 1
        for i in range(m):
            for j in range(n):
                if obstacleGrid[i][j]:
                    ans[j] = 0
                else:
                    if j>0:
                        ans[j] += ans[j-1]
        return ans[n-1]