class Solution:
    def nextPermutation(self, nums: List[int]) -> None:
        """
        Do not return anything, modify nums in-place instead.
        """
        if len(nums) <= 1:
            return nums
        index = len(nums)-2
        while index>=0:
            if nums[index]>=nums[index+1]:
                index -= 1
            else:
                break
        if index == -1:
            return nums.reverse()
        #indexb = len(nums)-1
        for i in range(len(nums)-1, index,-1):
            if nums[i]>nums[index]:
                indexb = i
                break
        tmp = nums[index]
        nums[index] = nums[indexb]
        nums[indexb] = tmp
        a = (len(nums)-index-1)//2
        for i in range(index+1,index+a+1):
            tmp = nums[i]
            nums[i] = nums[index+len(nums)-i]
            nums[index+len(nums)-i] = tmp
        return nums