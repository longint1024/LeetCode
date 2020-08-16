class Solution:
    def numIdenticalPairs(self, nums: List[int]) -> int:
        n, ans = len(nums), 0
        for i in range(n):
            for j in range(i+1,n):
                if nums[i] == nums[j]:
                    ans+=1
        return ans