class Solution:
    ans = []
    def permuteUnique(self, nums: List[int]) -> List[List[int]]:
        self.ans = []
        self.p([],nums)
        return self.ans
    def p(self, pre:List[int], nums:List[int]) -> None:
        n = len(nums)
        if n==1:
            self.ans.append(pre+[nums[0]])
            return
        exist = set()
        for i in range(n):
            if not (nums[i] in exist):
                exist.add(nums[i])
                num = nums[0:i]+nums[i+1:n]
                pre_next = pre+[nums[i]]
                self.p(pre_next,num)