from collections import deque
class Solution:
    def maxSlidingWindow(self, nums: List[int], k: int) -> List[int]:
        n = len(nums)
        if not (n and k):
            return []
        if k==1:
            return nums
        dq, ans = deque(), []
        def cleardq(i:int)->None:
            if dq and dq[0]==i-k:
                dq.popleft()
            while dq and nums[i]>nums[dq[-1]]:
                dq.pop()
        MAX = -1000000
        for i in range(k):
            cleardq(i)
            dq.append(i)
            if nums[i]>MAX:
                MAX = nums[i]
        ans.append(MAX)
        for i in range(k,len(nums)):
            cleardq(i)
            dq.append(i)
            ans.append(nums[dq[0]])
        return ans