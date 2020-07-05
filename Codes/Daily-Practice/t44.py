class Solution:
    def isMatch(self, s: str, p: str) -> bool:
        m, n = len(s), len(p)
        dp, e = [[0 for i in range(n+1)]for j in range(m+1)], [0 for i in range(n+1)]
        dp[0][0], e[0] = 1, 1
        for i in range(n):
            if p[i] == '*':
                dp[0][i+1] = 1
                e[i+1] = 1
            else:
                break
        for i in range(m):
            for j in range(n):
                if s[i] == p[j] or p[j] == '?':
                    dp[i+1][j+1] = dp[i][j]
                else:
                    if p[j] == '*':
                        if e[j]:
                            dp[i+1][j+1] = 1
                if dp[i+1][j+1]:
                    e[j+1] = 1
        return dp[m][n]==1