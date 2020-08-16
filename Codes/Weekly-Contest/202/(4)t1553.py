class Solution:
    def minDays(self, n: int) -> int:
        compute = {}
        def mind(n:int) -> int:
            if n in compute:
                return compute[n]
            if n == 1:
                return 1
            if n == 2 or n == 3:
                return 2
            c2 = mind(n//2)+ (n&1)
            c3 = mind(n//3) + n%3
            tmp = 1+min(c2,c3)
            compute[n] = tmp
            return tmp
        return mind(n)