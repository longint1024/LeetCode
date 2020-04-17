class Solution:
    def canJump(self, nums: List[int]) -> bool:
        l, r, n = 0, 0, len(nums)-1
        if nums == []:
            return True
        while 1:
            MAX = -1
            for i in range(l,r+1):
                if nums[i]+i>MAX:
                    MAX = nums[i]+i
            if MAX >= n:
                return True
            if MAX == r:
                return False
            l = r+1
            r = MAX