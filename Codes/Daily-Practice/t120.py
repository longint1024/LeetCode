class Solution:
    def minimumTotal(self, triangle: List[List[int]]) -> int:
        n = len(triangle)
        if n == 1:
            return triangle[0][0]
        dp = [0 for i in range(n)]
        dp[0] = triangle[0][0]
        ans = 10000000000
        for i in range(1,n):
            dp[i] = dp[i-1]+triangle[i][i]
            if i==n-1 and dp[i]<ans:
                ans = dp[i]
            for j in range(i-1,0,-1):
                dp[j] = min(dp[j-1], dp[j])+triangle[i][j]
                if i==n-1 and dp[j]<ans:
                    ans = dp[j]
            dp[0] = dp[0]+triangle[i][0]
            if i==n-1 and dp[0]<ans:
                ans = dp[0]
        return ans