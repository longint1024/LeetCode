class Solution:
    def movingCount(self, m: int, n: int, k: int) -> int:
        ans = 1
        dirx = [0,0,1,-1]
        diry = [1,1,0,0]
        def ss(n:int)-> bool:
            p = 0
            while(n>0):
                p += n%10
                n = n//10
            return p
        queue = [[0,0]]
        front, rear = -1, 0
        arr = [[0 for i in range(n)]for j in range(m)]
        arr[0][0] = 1
        def judge(x:int,y:int)->bool:
            if x<0 or y<0 or x>=m or y>=n:
                return False
            if arr[x][y]:
                return False
            return True
        while front < rear:
            front += 1
            x, y = queue[front][0], queue[front][1]
            for i in range(4):
                xx, yy = x+dirx[i], y+diry[i]
                if judge(xx,yy):
                    if ss(xx)+ss(yy)<=k:
                        rear += 1
                        queue.append([xx,yy])
                        ans += 1
                    arr[xx][yy] = 1
        return ans