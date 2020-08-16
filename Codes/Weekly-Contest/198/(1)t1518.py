class Solution:
    def numWaterBottles(self, numBottles: int, numExchange: int) -> int:
        now, left, ans = numBottles, 0, 0
        while now>0:
            left += now
            ans += now
            now = left // numExchange
            left = left - now*numExchange
        return ans