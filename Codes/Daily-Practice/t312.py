class Solution:
    def maxCoins(self, nums: List[int]) -> int:
        n = len(nums)
        nums.insert(0,1)
        nums.append(1)
        dp = [[0 for i in range(n+2)]for j in range(n+2)]
        for i in range(n+1,-1,-1):
            for j in range(i+2,n+2):
                for k in range(i+1,j):
                    if dp[i][k]+dp[k][j]+nums[i]*nums[j]*nums[k]>dp[i][j]:
                        dp[i][j] = dp[i][k]+dp[k][j]+nums[i]*nums[j]*nums[k]
        return dp[0][n+1]