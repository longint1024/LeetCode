class Solution:
    def firstMissingPositive(self, nums: List[int]) -> int:
        nums = set(nums)
        i=1;
        while 1:
            if i in nums:
                i = i+1
                continue
            else:
                break
        return i