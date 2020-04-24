class Solution:
    def reversePairs(self, nums: List[int]) -> int:
        def merge(l:int,mid:int,r:int)->int:
            i,j,tmp,count = l,mid+1,[],0
            while 1:
                while i<=mid and nums[i]<=nums[j]:
                    tmp.append(nums[i])
                    i+=1
                if i>mid:
                    break
                while j<=r and nums[j]<nums[i]:
                    tmp.append(nums[j])
                    j+=1
                    count += mid-i+1
                if j>r:
                    break
            if j>r:
                tmp = tmp+nums[i:mid+1]
            if i>mid:
                tmp = tmp+nums[j:r+1]
            nums[l:r+1] = tmp
            return count
        def mergesort(l:int,r:int)->int:
            if l>=r:
                return 0
            mid = (l+r)//2
            tmp = 0
            tmp += mergesort(l,mid)
            tmp += mergesort(mid+1,r)
            tmp += merge(l,mid,r)
            return tmp
        return mergesort(0,len(nums)-1)