class Solution:
    def searchInsert(self, nums: List[int], target: int) -> int:
        if nums==[]:
            return 0
        return self.find(nums,target)
    def find(self, nums: List[int], target: int) -> int:
        n = len(nums)
        if target <= nums[0]:
            return 0
        if target > nums[n-1]:
            return n
        half = n//2
        if target>nums[half]:
            return half+self.find(nums[half:n],target)
        if target<=nums[half]:
            return self.find(nums[0:half],target)
        