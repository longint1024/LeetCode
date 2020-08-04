class Solution:
    def integerBreak(self, n: int) -> int:
        ans = [1 for i in range(60)]
        for i in range(2,n+1):
            MAX = 0
            for j in range(1,i//2+1):
                tmp = max(ans[j],j)*max(ans[i-j],i-j)
                if tmp>MAX:
                    MAX = tmp
            ans[i] = MAX
        return ans[n]