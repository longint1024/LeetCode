class Solution:
    def dominantIndex(self, nums: List[int]) -> int:
        MAX1 , MAX2 = -1, -1
        index1, index2 = -1, -1
        for i in range(len(nums)):
            if nums[i]>MAX1:
                MAX2, index2 = MAX1, index1
                MAX1, index1 = nums[i], i
                continue
            if nums[i]>MAX2:
                MAX2, index2 = nums[i], i
        if MAX1 >= 2*MAX2:
            return index1
        else:
            return -1