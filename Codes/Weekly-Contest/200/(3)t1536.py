class Solution:
    def minSwaps(self, grid: List[List[int]]) -> int:
        n = len(grid)
        count = [0 for _ in range(n)]
        for i in range(n):
            for j in range(n):
                if not grid[i][n-1-j]:
                    count[i] += 1
                else:
                    break
        ans = 0
        for i in range(n):
            need = n-i-1
            flag = 0
            for j in range(i,n):
                if count[j]>=need:
                    flag = 1
                    ans += j-i
                    tmp = count[j]
                    del count[j]
                    count.insert(i,tmp)
                    break
            if not flag:
                return -1
        return ans