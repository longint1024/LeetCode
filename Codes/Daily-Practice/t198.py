class Solution:
    def rob(self, nums: List[int]) -> int:
        if nums == []:
            return 0
        if len(nums) == 1:
            return nums[0]
        MAX = max(nums[0], nums[1])
        first, second = nums[0], MAX
        for i in range(2,len(nums)):
            if first + nums[i] > MAX:
                MAX = first + nums[i]
            first = second
            second = MAX
        return MAX