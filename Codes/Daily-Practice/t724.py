class Solution:
    def pivotIndex(self, nums: List[int]) -> int:
        n, s = len(nums), sum(nums)
        if n<2:
            return -1
        index = 0
        ss = 0
        while index<n:
            if ss == s-nums[index]:
                return index
            ss += 2*nums[index]
            index += 1
        return -1