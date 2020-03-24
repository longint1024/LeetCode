class Solution:
    def fib(self, n: int) -> int:
        def multi(x:List[List[int]], y:List[List[int]]) -> List[List[int]]:
            m = len(x)
            n = len(x[0])
            s = len(y[0])
            tmp = [[0 for i in range(s)]for j in range(m)]
            for i in range(m):
                for j in range(n):
                    for k in range(s):
                        tmp[i][k] += x[i][j]*y[j][k] % 1000000007
            return tmp
        fib = [[0,1],[1,1]]
        a = [[0],[1]]
        while n>0:
            if n & 1 == 1:
                a = multi(fib,a)
            n = n//2
            fib = multi(fib,fib)
        return a[0][0] % 1000000007