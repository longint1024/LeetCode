class Solution:
    def moveZeroes(self, nums: List[int]) -> None:
        """
        Do not return anything, modify nums in-place instead.
        """
        point1, point2, n = 0, 0, len(nums)
        while point2<n:
            if nums[point2]!=0:
                if point1<point2:
                    nums[point1], nums[point2] = nums[point2], nums[point1]
                    
                point1 += 1
            point2 += 1