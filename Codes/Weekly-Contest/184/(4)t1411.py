class Solution:
    def numOfWays(self, n: int) -> int:
        p = ['ryr','ryg','rgr','rgy','yry','yrg','ygr','ygy','gry','grg','gyr','gyg']
        m = [[0 for i in range(12)]for j in range(5004)]
        T = 10**9 + 7
        for i in range(12):
            m[0][i] = 1
        def keyi(i:int,j:int)->bool:
            for k in range(3):
                if p[i][k] == p[j][k]:
                    return False
            return True
        for i in range(1,n):
            for j in range(12):
                for k in range(12):
                    if keyi(j,k):
                        m[i][j] += m[i-1][k]
                m[i][j] = m[i][j] % T
        ans = 0
        for i in range(12):
            ans += m[n-1][i]
        ans = ans%T
        return ans