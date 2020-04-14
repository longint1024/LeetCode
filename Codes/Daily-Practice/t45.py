class Solution:
    def jump(self, nums: List[int]) -> int:
        if len(nums)<=1:
            return 0
        l, r, step = 0, 0, 0
        while 1:
            next = r+1
            for i in range(l,r+1):
                if i+nums[i]>next:
                    next = i+nums[i]
            step += 1
            if next>=len(nums)-1:
                return step
            l = r+1
            r = next