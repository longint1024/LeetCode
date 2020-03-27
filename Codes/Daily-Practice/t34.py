class Solution:
    def searchRange(self, nums: List[int], target: int) -> List[int]:
        if nums == []:
            return [-1,-1]
        n = len(nums)
        ans = []
        def findl(l:int,r:int)->int:
            for i in range(l,r+1):
                if nums[i]==target:
                    return i
            return -1
        def findr(l:int,r:int)->int:
            for i in range(r,l-1,-1):
                if nums[i]==target:
                    return i
            return -1
        def findleft(l:int, r:int) -> int:
            if r-l < 10:
                return findl(l,r)
            mid = (l+r)//2
            if target<=nums[mid]:
                return findleft(l,mid)
            else:
                return findleft(mid,r)
        def findright(l:int, r:int) -> int:
            if r-l < 10:
                return findr(l,r)
            mid = (l+r)//2
            if target>=nums[mid]:
                return findright(mid,r)
            else:
                return findright(l,mid)
        ans.append(findleft(0,n-1))
        ans.append(findright(0,n-1))
        return ans