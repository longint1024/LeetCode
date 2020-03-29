class Solution:
    def surfaceArea(self, grid: List[List[int]]) -> int:
        n = len(grid)
        ans = 0
        def hh(x:int,y:int,h:int)->int:
            if x<0 or y<0 or x>n-1 or y>n-1 or grid[x][y]==0:
                return h
            return max(h-grid[x][y],0)
        def high(x:int, y:int)->int:
            h = grid[x][y]
            return hh(x-1,y,h)+hh(x+1,y,h)+hh(x,y-1,h)+hh(x,y+1,h)
        for i in range(n):
            for j in range(n):
                if grid[i][j]:
                    ans += 2+high(i,j)
        return ans