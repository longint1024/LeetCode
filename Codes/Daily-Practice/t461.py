class Solution:
    def hammingDistance(self, x: int, y: int) -> int:
        t=x^y
        ans=0
        while(t>0):
            ans=ans+(t&1)
            t=t>>1
        return ans