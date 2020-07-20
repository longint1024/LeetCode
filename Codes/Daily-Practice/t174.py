class Solution:
    def calculateMinimumHP(self, dungeon: List[List[int]]) -> int:
        m, n = len(dungeon), len(dungeon[0])
        dp = [1000000000 for i in range(n+1)]
        dp[n] = 1
        i = m-1
        for j in range(n-1,-1,-1):
            minn = min(dp[j],dp[j+1])
            dp[j] = max(minn-dungeon[i][j],1)
        dp[n] = 100000000
        for i in range(m-2,-1,-1):
            for j in range(n-1,-1,-1):
                minn = min(dp[j],dp[j+1])
                dp[j] = max(minn-dungeon[i][j],1)
        return dp[0]