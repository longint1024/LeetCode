class Solution:
    def numTrees(self, n: int) -> int:
        ans = 1
        for i in range(2,n+1):
            ans = ans*(4*i-2)//(i+1)
        return ans