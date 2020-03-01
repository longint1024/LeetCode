class Solution:
    def rotate(self, matrix: List[List[int]]) -> None:
        """
        Do not return anything, modify matrix in-place instead.
        """
        n = len(matrix)
        if n==0:
            return [[]]
        if n==1:
            return matrix
        for i in range(n//2):
            for j in range((n+1)//2):
                x1, y1 = i, j
                x2, y2 = j, n-i-1
                x3, y3 = n-i-1, n-j-1
                x4, y4 = n-j-1, i
                temp = matrix[x4][y4]
                matrix[x4][y4] = matrix[x3][y3]
                matrix[x3][y3] = matrix[x2][y2]
                matrix[x2][y2] = matrix[x1][y1]
                matrix[x1][y1] = temp