class Solution:
    def rangeBitwiseAnd(self, m: int, n: int) -> int:
        x = n-m
        ans = m&n
        cnt = 0
        while x>0:
            x = x >> 1
            ans = ans >> 1
            cnt += 1
        while cnt>0:
            ans = ans << 1
            cnt -= 1
        return ans