class Solution:
    def findRepeatNumber(self, nums: List[int]) -> int:
        exist = set()
        for i in nums:
            if i in exist:
                return i
            exist.add(i)