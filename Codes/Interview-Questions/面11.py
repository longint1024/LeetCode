class Solution:
    def minArray(self, numbers: List[int]) -> int:
        def findmin(l:int, r:int) ->int:
            MIN = 2147483648
            for i in range(l,r+1):
                if numbers[i]<MIN:
                    MIN = numbers[i]
            return MIN
        def find(l:int, r:int) ->int:
            if l==r:
                return numbers[l]
            mid = (l+r)//2
            if numbers[mid]==numbers[r] or r-l<10:
                return findmin(l,r)
            if numbers[mid]>numbers[r]:
                return find(mid,r)
            if numbers[mid]<numbers[r]:
                return find(l,mid)
        return find(0,len(numbers)-1)