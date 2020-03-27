class Solution:
    def maxAreaOfIsland(self, grid: List[List[int]]) -> int:
        print(grid)
        m = len(grid)
        n = len(grid[0])
        map = [[0 for i in range(n)]for j in range(m)]
        dx = [0,0,1,-1]
        dy = [-1,1,0,0]
        MAX = 0
        def judge(x:int, y:int) -> bool:
            if x>m-1 or y>n-1 or x<0 or y<0:
                return False
            if map[x][y] or not grid[x][y]:
                return False
            map[x][y] = 1
            return True
            
        def bfs(x:int, y:int) -> int:
            queue = [[x,y]]
            map[x][y] = 1
            front = -1
            rear = 0
            while front<rear:
                front += 1
                xx = queue[front][0]
                yy = queue[front][1]
                for i in range(4):
                    if judge(xx+dx[i],yy+dy[i]):
                        rear += 1
                        queue.append([xx+dx[i],yy+dy[i]])
            return rear+1
        for i in range(m):
            for j in range(n):
                if grid[i][j] and not map[i][j]:
                    area = bfs(i,j)
                    if area>MAX:
                        MAX = area
        return MAX