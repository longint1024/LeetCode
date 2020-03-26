class Solution:
    def findMin(self, nums: List[int]) -> int:
        def findmin(l:int, r:int) ->int:
            MIN = 2147483648
            for i in range(l,r+1):
                if nums[i]<MIN:
                    MIN = nums[i]
            return MIN
        def find(l:int, r:int) ->int:
            if l==r:
                return nums[l]
            mid = (l+r)//2
            if r-l<10:
                return findmin(l,r)
            if nums[mid]>nums[r]:
                return find(mid,r)
            if nums[mid]<nums[r]:
                return find(l,mid)
            if nums[mid] == nums[r]:
                return findmin(l,r)
        return find(0,len(nums)-1)