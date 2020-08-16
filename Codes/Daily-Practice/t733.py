class Solution:
    def floodFill(self, image: List[List[int]], sr: int, sc: int, newColor: int) -> List[List[int]]:
        if image[sr][sc] == newColor:
            return image
        m, n = len(image), len(image[0])
        newimage = [[image[i][j] for j in range(n)]for i in range(m)]
        havebeen = [[0 for j in range(n)]for i in range(m)]
        def judge(x:int,y:int,t:int)->bool:
            if x>m-1 or y>n-1 or x<0 or y<0:
                return False
            if image[x][y]!=t:
                return False
            return True
        dx, dy = [-1,1,0,0], [0,0,1,-1]
        def dfs(x:int,y:int)->None:
            havebeen[x][y] = 1
            newimage[x][y] = newColor
            for i in range(4):
                nx, ny = x+dx[i],y+dy[i]
                if judge(nx,ny,image[x][y]) and not havebeen[nx][ny]:
                    dfs(nx,ny)
            return        
        dfs(sr,sc)
        return newimage