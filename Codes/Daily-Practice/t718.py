class Solution:
    def findLength(self, A: List[int], B: List[int]) -> int:
        m, n, MAX = len(A), len(B), 0
        dp = [[0 for i in range(n+1)]for j in range(m+1)]
        for i in range(1,m+1):
            for j in range(1,n+1):
                if A[i-1]==B[j-1]:
                    dp[i][j] = dp[i-1][j-1]+1
                else:
                    dp[i][j] = 0
                if dp[i][j]>MAX:
                    MAX = dp[i][j]
        return MAX