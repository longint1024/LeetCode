class Solution:
    def findDiagonalOrder(self, matrix: List[List[int]]) -> List[int]:
        if matrix == []:
            return []
        m, n = len(matrix), len(matrix[0])
        def judge(x:int,y:int)->bool:
            if x<0 or y<0 or x>m-1 or y>n-1:
                return False
            return True
        x, y, ans, num = 0, 0, [matrix[0][0]], 1
        while num<m*n:
            if judge(x,y+1):
                y = y+1
                ans.append(matrix[x][y])
                num += 1
            else:
                if judge(x+1,y):
                    x = x+1
                    ans.append(matrix[x][y])
                    num += 1
            while judge(x+1,y-1):
                x, y = x+1, y-1
                ans.append(matrix[x][y])
                num += 1
                
            if judge(x+1,y):
                x = x+1
                ans.append(matrix[x][y])
                num += 1
            else:
                if judge(x,y+1):
                    y = y+1
                    ans.append(matrix[x][y])
                    num += 1
            while judge(x-1,y+1):
                x, y = x-1, y+1
                ans.append(matrix[x][y])
                num += 1
        return ans         