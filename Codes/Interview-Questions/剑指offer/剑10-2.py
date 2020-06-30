class Solution:
    a = [1,1]
    i = 0
    while 1:
        a.append((a[i]+a[i+1])%1000000007)
        i += 1
        if i>100:
            break
    def numWays(self, n: int) -> int:
        return self.a[n]