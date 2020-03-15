class Solution:
    def luckyNumbers (self, matrix: List[List[int]]) -> List[int]:
        m = len(matrix)
        n = len(matrix[0])
        ans = []
        for i in range(m):
            for j in range(n):
                num = matrix[i][j]
                flag = 1
                for k in range(m):
                    if num<matrix[k][j]:
                        flag= 0
                        break
                for k in range(n):
                    if num>matrix[i][k]:
                        flag= 0
                        break
                if flag:
                    ans.append(num)
        return ans