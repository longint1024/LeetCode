class Solution:
    def numIslands(self, grid: List[List[str]]) -> int:
        if grid == []:
            return 0
        m, n = len(grid), len(grid[0])
        gmap = [[0 for i in range(n)]for j in range(m)]
        def judge(x:int, y:int)->bool:
            if x<0 or y<0 or x>m-1 or y>n-1:
                return False
            if gmap[x][y]:
                return False
            return grid[x][y]=='1'
        ans = 0
        dx, dy = [0,0,1,-1], [1,-1,0,0]
        for i in range(m):
            for j in range(n):
                if (not gmap[i][j]) and grid[i][j]=='1':
                    queue, front, rear = [[i,j]], -1, 0
                    gmap[i][j] = 1
                    ans += 1
                    while front<rear:
                        front+=1
                        x,y = queue[front][0], queue[front][1]
                        for k in range(4):
                            xx, yy = x+dx[k],y+dy[k]
                            if judge(xx,yy):
                                gmap[xx][yy] = 1
                                rear += 1
                                queue.append([xx,yy])
        return ans           