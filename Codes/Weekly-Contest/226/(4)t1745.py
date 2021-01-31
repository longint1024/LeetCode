class Solution:
    def checkPartitioning(self, s: str) -> bool:
        n = len(s)
        dp = [[0 for i in range(n)]for j in range(n)]
        for i in range(n):
            dp[i][i] = 1
        for i in range(1,n-1):
            for j in range(n-1):
                if j+i<n:
                    if i==1:
                        dp[j][j+1] = s[j] == s[j+i]
                    else:
                        dp[j][j+i] = dp[j+1][j+i-1] and s[j] == s[j+i]
        for i in range(n):
            for j in range(n):
                if dp[0][i] and dp[i+1][j] and dp[j+1][n-1]:
                    return True
        return False