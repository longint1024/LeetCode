class Solution:
    def numEquivDominoPairs(self, dominoes: List[List[int]]) -> int:
        count = [0 for i in range(100)]
        def map(x,y):
            if x<=y:
                return x*10+y
            return y*10+x
        for d in dominoes:
            count[map(d[0],d[1])] += 1
        ans = 0
        for i in count:
            ans += i*(i-1)//2;
        return ans