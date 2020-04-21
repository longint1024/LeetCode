class Solution:
    def numberOfSubarrays(self, nums: List[int], k: int) -> int:
        count = 0
        dp = []
        n, ans = 0, 0
        for i in nums:
            if i&1 == 0:
                count+=1
            else:
                dp.append(count)
                count = 0
                n+=1
            if n>=k:
                    ans += dp[n-k]+1
        return ans