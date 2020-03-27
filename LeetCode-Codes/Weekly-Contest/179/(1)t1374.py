class Solution:
    def generateTheString(self, n: int) -> str:
        a = 'x'
        b = 'y'
        ans = ''
        if n & 1 == 0:
            for i in range(n-1):
                ans = ans + a
            ans = ans + b
        else:
            for i in range(n):
                ans = ans + a
        return ans