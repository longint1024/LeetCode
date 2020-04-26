class Solution:
    def findDiagonalOrder(self, nums: List[List[int]]) -> List[int]:
        nn = []
        for i in range(len(nums)):
            for j in range(len(nums[i])):
                nn.append([i+j,j,nums[i][j]])
        nn.sort()
        ans = []
        for i in nn:
            ans.append(i[2])
        return ans