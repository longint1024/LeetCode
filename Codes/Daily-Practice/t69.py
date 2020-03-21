class Solution:
    def mySqrt(self, x: int) -> int:
        if x<2:
            return x
        x0 = x//2
        while 1:
            x0 = int((x0*x0 + x)/(2*x0))
            if x0*x0 == x:
                return x0
            if x0*x0 > x and (x0-1)*(x0-1)<x:
                return x0-1
            if x0*x0 < x and (x0+1)*(x0+1)>x:
                return x0