class Solution:
    def findNumberIn2DArray(self, matrix: List[List[int]], target: int) -> bool:
        if matrix == [] or matrix == [[]]:
            return False
        n = len(matrix)
        m = len(matrix[0])
        for index in range(n):
            if target>matrix[index][m-1] or target<matrix[index][0]:
                continue
            l = 0
            r = m-1
            if target == matrix[index][r] or target == matrix[index][l]:
                return True
            while l<r:
                if target == matrix[index][r] or target == matrix[index][l]:
                    return True
                mid = (l+r)//2
                if target == matrix[index][mid]:
                    return True
                if target < matrix[index][mid]:
                    r = mid
                if target > matrix[index][mid]:
                    l = mid
                if r == l+1 and target != matrix[index][r]:
                    break
        return False