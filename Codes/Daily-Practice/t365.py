class Solution:
    def canMeasureWater(self, x: int, y: int, z: int) -> bool:
        if x+y<z:
            return False
        if y==0 and x==0:
            return z==0
        if y==0:
            return z%x == 0
        if x==0:
            return z%y == 0
        def gcd(a:int,b:int)->int:
            return gcd(b,a%b) if b else a
        m = gcd(x,y)
        if z%m == 0:
            return True
        else:
            return False