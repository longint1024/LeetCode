class Solution:
    def removeElement(self, nums: List[int], val: int) -> int:
        index = 0
        while 1:
            while index<len(nums) and nums[index]==val:
                del(nums[index])
            if index>=len(nums):
                break
            index = index +1
        return len(nums)