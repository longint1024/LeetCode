class Solution:
    def fourSum(self, nums: List[int], target: int) -> List[List[int]]:
        nums.sort()
        ans = set()
        n = len(nums)
        for i in range(n-3):
            a = nums[i]
            if (i>0 and nums[i]==nums[i-1]):
                continue
            for j in range(i+1,n-2):
                b, index = nums[j], n-1
                if (j>i+1 and nums[j]==nums[j-1]):
                    continue
                for k in range(j+1,n-1):
                    c = nums[k]
                    d = target-a-b-c
                    if(d<c):
                        break
                    while index>k+1 and nums[index]>d:
                        index = index-1
                    if (index>k and nums[index]==d):
                        ans.add((a,b,c,d))
        return list(ans)