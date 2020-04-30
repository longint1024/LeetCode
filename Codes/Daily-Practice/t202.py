class Solution:
    def isHappy(self, n: int) -> bool:
        def next(num:int)->int:
            tot = 0
            while num>0:
                tot += (num%10)**2
                num //= 10
            return tot
        showup = set()
        showup.add(n)
        while n!=1:
            n = next(n)
            if n in showup:
                return False
            showup.add(n)
        return True