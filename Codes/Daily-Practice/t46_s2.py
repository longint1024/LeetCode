class Solution:
    def permute(self, nums: List[int]) -> List[List[int]]:
        n = len(nums)
        used = [0]*n
        ans = []
        p = []
        def dfs()->None:
            for i in range(n):
                if not used[i]:
                    ans.append(nums[i])
                    used[i] = 1
                    dfs()
                    used[i] = 0
                    ans.remove(nums[i])
            if len(ans)==n:
                tmp = [ans[k] for k in range(n)]
                p.append(tmp)
        dfs()
        return p