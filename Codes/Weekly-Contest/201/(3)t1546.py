class Solution:
    def maxNonOverlapping(self, nums: List[int], target: int) -> int:
        now, SUM, ans = 0, {0}, 0
        for n in nums:
            now += n
            if now-target in SUM:
                now, SUM = 0, {0}
                ans += 1
            else:
                SUM.add(now)
        return ans