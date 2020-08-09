class Solution:
    def minCost(self, n: int, cuts: List[int]) -> int:
        l = n
        n = len(cuts)
        cuts.sort()
        cuts.insert(0,0)
        cuts.append(l)
        print(cuts)
        tMAX = 10000000
        d = [[tMAX for i in range(n+2)]for j in range(n+2)]
        for i in range(n+1):
            d[i][i+1] = 0
        def dp(i:int,j:int)->int:
            if d[i][j]<tMAX:
                return d[i][j]
            for k in range(i+1,j):
                d[i][j] = min (d[i][j], dp (i, k) + dp (k , j) + cuts[j] - cuts[i])
            return d[i][j]
        return dp(0,n+1)