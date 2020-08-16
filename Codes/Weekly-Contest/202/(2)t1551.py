class Solution:
    def minOperations(self, n: int) -> int:
        ans = 0
        for i in range(1,n+1):
            ans += abs(2*i-1-n)
        return ans//2