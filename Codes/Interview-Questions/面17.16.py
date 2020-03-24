class Solution:
    def massage(self, nums: List[int]) -> int:
        ans = nums
        MAX = -2147483647
        for i in range(2,len(nums)):
            if ans[i-2]>MAX:
                MAX = ans[i-2]
            ans[i] += MAX
        MAX = 0
        for i in range(len(nums)):
            if ans[i]>MAX:
                MAX = ans[i]
        return MAX