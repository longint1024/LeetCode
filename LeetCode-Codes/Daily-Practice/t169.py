class Solution:
    def majorityElement(self, nums: List[int]) -> int:
        ll = len(nums)
        e = set()
        for i in nums:
            if not i in e and nums.count(i)>ll//2:
                return i
            else:
                e.add(i)