class Solution:
    def threeSumClosest(self, nums: List[int], target: int) -> int:
        nums.sort()
        n = len(nums)
        min = 2147483647
        for i in range(n):
            if i>0 and nums[i]==nums[i-1]:
                continue
            index = n-1
            for j in range(i+1,n-1):
                a, b = nums[i], nums[j]
                err = abs(target-a-b-nums[index])
                while index>j+1:
                    new = index-1
                    err_new = abs(target-a-b-nums[new])
                    if err_new>err:
                        break
                    index = new
                    err = err_new
                if err<min:
                    min = err
                    ans = a+b+nums[index]
        return ans