class Solution:
    def countBalls(self, lowLimit: int, highLimit: int) -> int:
        def count(n):
            r = 0
            while n>0:
                temp = n//10
                r += n - temp*10
                n = temp
            return r
        ss = [0 for i in range(50)]
        for i in range(lowLimit, highLimit+1):
            ss[count(i)] += 1
        ans = 0
        #print(ss)
        for s in ss:
            if s>ans:
                ans = s
        return ans