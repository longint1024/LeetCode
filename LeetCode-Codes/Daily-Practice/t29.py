class Solution:
    def divide(self, dividend: int, divisor: int) -> int:
        MAX=2**31-1
        MIN=-(2**31)
        ans = dividend//divisor
        if ans<0:
            divisor = -divisor
            ans = dividend//divisor
            ans = -ans
        if ans>MAX:
            return MAX
        if ans<MIN:
            return MIN
        return ans