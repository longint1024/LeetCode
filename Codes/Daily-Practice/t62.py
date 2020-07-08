class Solution:
    def uniquePaths(self, m: int, n: int) -> int:
        ans = [1 for i in range(n)]
        for i in range(1,m):
            for j in range(n):
                if j>0:
                    ans[j] += ans[j-1]
        return ans[n-1]