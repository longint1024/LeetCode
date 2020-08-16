class Solution:
    def solve(self, board: List[List[str]]) -> None:
        if board == []:
            return []
        m, n = len(board), len(board[0])
        dx, dy = [-1,1,0,0], [0,0,1,-1]
        havebeen = [[0 for i in range(n)]for j in range(m)]
        def judge(x:int,y:int)->bool:
            if x<0 or y<0 or x>m-1 or y>n-1:
                return False
            if board[x][y]=='O' and not havebeen[x][y]:
                return True
            return False
        def dfs(x:int,y:int)->None:
            havebeen[x][y] = 1
            for k in range(4):
                if judge(x+dx[k],y+dy[k]):
                    dfs(x+dx[k],y+dy[k])
            return
        for i in range(n):
            if judge(0,i):
                dfs(0,i)
            if judge(m-1,i):
                dfs(m-1,i)
        for i in range(m):
            if judge(i,0):
                dfs(i,0)
            if judge(i,n-1):
                dfs(i,n-1)
        for i in range(m):
            for j in range(n):
                if board[i][j] =='O' and not havebeen[i][j]:
                    board[i][j] = 'X'