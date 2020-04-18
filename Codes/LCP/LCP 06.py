class Solution:
    def minCount(self, coins: List[int]) -> int:
        ans = 0
        for i in coins:
            ans += (i+1)//2
        return ans