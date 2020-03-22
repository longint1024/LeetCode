class Solution:
    def hasValidPath(self, grid: List[List[int]]) -> bool:
        m, n = len(grid), len(grid[0])
        if m == 1 and n ==1 :
            return True
        map = [[0 for i in range(n)]for j in range(m)]
        path1 = [[1,0,0,1,0,1],[0,1,1,1,0,0],[1,0,0,1,0,1],[0,1,0,0,1,1],[1,0,0,1,0,1],[0,1,1,1,0,0]]
        dir1x = [0,-1,0,1,0,-1]
        dir1y = [-1,0,-1,0,-1,0]
        path2 = [[1,0,1,0,1,0],[0,1,0,0,1,1],[0,1,0,0,1,1],[1,0,1,0,1,0],[0,1,1,1,0,0],[1,0,1,0,1,0]]
        dir2x = [0,1,1,0,-1,0]
        dir2y = [1,0,0,1,0,1]
        queue = [[0,0]]
        map[0][0] = 1
        front = -1
        rear = 0
        def judge(x1:int,y1:int,x2:int,y2:int,t:int)->bool:
            if x2>=m or y2>=n or x2<0 or y2<0:
                return False
            if map[x2][y2]:
                return False
            if t == 1:
                if path1[grid[x1][y1]-1][grid[x2][y2]-1]:
                    return True
                else:
                    return False
            else:
                if path2[grid[x1][y1]-1][grid[x2][y2]-1]:
                    return True
                else:
                    return False
        while front<rear:
            front += 1
            x = queue[front][0]
            y = queue[front][1]
            k = grid[x][y]-1
            if judge(x,y,x+dir1x[k],y+dir1y[k],1):
                rear+=1
                queue.append([x+dir1x[k], y+dir1y[k]])
                map[x+dir1x[k]][y+dir1y[k]] = 1
                if x+dir1x[k] == m-1 and y+dir1y[k] == n-1:
                    return True
            if judge(x,y,x+dir2x[k],y+dir2y[k],2):
                rear+=1
                queue.append([x+dir2x[k], y+dir2y[k]])
                map[x+dir2x[k]][y+dir2y[k]] = 1
                if x+dir2x[k] == m-1 and y+dir2y[k] == n-1:
                    return True
        return False