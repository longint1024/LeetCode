class Solution:
    def minPathSum(self, grid: List[List[int]]) -> int:
        m, n = len(grid), len(grid[0])
        dp = [0 for i in range(n)]
        dp[0] = grid[0][0]
        for i in range(1,n):
            dp[i] = dp[i-1]+grid[0][i]
        for i in range(1,m):
            for j in range(n):
                if j>0:
                    dp[j] = min(dp[j],dp[j-1]) + grid[i][j]
                else:
                    dp[j] += grid[i][j]
        return dp[n-1]