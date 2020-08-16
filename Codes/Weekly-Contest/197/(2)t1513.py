class Solution:
    def numSub(self, s: str) -> int:
        ans = [0 for i in range(100004)]
        M = 10**9 + 7
        for i in range(100003):
            ans[i] = (i+1)*i//2
        cnt, tot = 0, 0
        for i in s:
            if i == '0':
                tot += ans[cnt]
                tot = tot % M
                cnt = 0
            else:
                cnt += 1
        if cnt>0:
            tot += ans[cnt]
        return (tot%M)