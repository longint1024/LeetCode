from functools import reduce
class Solution:
    def singleNumbers(self, nums: List[int]) -> List[int]:
        xor, dif, ans1, ans2 = reduce(lambda x,y:x^y,nums), 1 ,0, 0
        while not dif & xor:
            dif <<= 1
        for i in nums:
            if i & dif:
                ans1 ^= i
            else:
                ans2 ^= i
        return [ans1,ans2]