class Solution:
    def spiralOrder(self, matrix: List[List[int]]) -> List[int]:
        if matrix == []:
            return []
        m, n = len(matrix), len(matrix[0])
        map = [[0 for i in range(n)] for j in range(m)]
        dirx, diry, x, y, d = [0,1,0,-1], [1,0,-1,0], 0, 0, 0
        map[x][y] = 1
        ans = [matrix[x][y]]
        def judge(x:int, y:int) -> bool:
            if x>=m or y>=n or x<0 or y<0:
                return False
            if map[x][y]:
                return False
            return True
        while 1:
            if judge(x+dirx[d], y+diry[d]):
                x, y = x+dirx[d], y+diry[d]
                ans.append(matrix[x][y])
                map[x][y] = 1
                continue
            else:
                d = (d+1) % 4
                if not judge(x+dirx[d], y+diry[d]):
                    break
                else:
                    continue
        return ans