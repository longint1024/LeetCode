class Solution:
    def maxSubArray(self, nums: List[int]) -> int:
        MAX = -2147483648
        n = len(nums)
        if nums == []:
            return MAX
        ans = nums[0]
        if ans>MAX:
            MAX = ans
        for i in range(1,n):
            if nums[i]+ans>nums[i]:
                ans = nums[i]+ans
            else:
                ans = nums[i]
            if ans>MAX:
                MAX = ans
        return MAX