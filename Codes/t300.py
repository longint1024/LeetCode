class Solution:
    def lengthOfLIS(self, nums: List[int]) -> int:
        if nums == []:
            return 0
        n =  len(nums)
        dp = [1 for j in range(n)]
        for i in range(n):
            for j in range(i+1,n):
                if nums[j]>nums[i] and dp[i]+1>dp[j]:
                    dp[j] = dp[i]+1
        MAX = 0
        for i in range(n):
            if dp[i]>MAX:
                MAX = dp[i]
        return MAX