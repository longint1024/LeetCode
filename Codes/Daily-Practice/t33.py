class Solution:
    def search(self, nums: List[int], target: int) -> int:
        if nums == []:
            return -1
        def findmin(l:int,r:int)->int:
            MIN = 2147483647
            index = 0
            for i in range(l,r+1):
                if nums[i]<MIN:
                    MIN = nums[i]
                    index = i
            return index
        def find(l:int,r:int)->int:
            if r-l<10:
                return findmin(l,r)
            mid = (l+r)//2
            if nums[mid]<nums[r]:
                return find(l,mid)
            else:
                return find(mid,r)
        index = find(0,len(nums)-1)
        def ist(l:int,r:int)->int:
            for i in range(l,r+1):
                if nums[i]==target:
                    return i
            return -1
        def findt(l:int,r:int)->int:
            if r-l<10:
                return ist(l,r)
            else:
                mid = (l+r)//2
                if target==nums[mid]:
                    return mid
                if target<nums[mid]:
                    return findt(l,mid)
            return findt(mid,r)
        f1 = findt(0,index)
        f2 = findt(index,len(nums)-1)
        if f1!=-1:
            return f1
        if f2!=-1:
            return f2
        return -1