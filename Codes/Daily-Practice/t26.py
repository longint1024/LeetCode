class Solution:
    def removeDuplicates(self, nums: List[int]) -> int:
        if len(nums)<=1:
            return len(nums)
        index = 1
        flag = 1
        while 1:
            while index<len(nums) and nums[index]==nums[index-1]:
                del(nums[index])
            if index<len(nums)-1:
                index = index + 1
            else:
                break
        return len(nums)