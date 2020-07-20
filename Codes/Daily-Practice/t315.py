class Solution:
    def countSmaller(self, nums: List[int]) -> List[int]:
        num_length = len(nums)
        if not nums:
            return []

        res = [0]*num_length
        sorted_nums = []
        for i in range(len(nums)-1, -1, -1):
            idx = bisect.bisect_left(sorted_nums, nums[i])
            sorted_nums.insert(idx, nums[i])
            res[i] = idx
        return res