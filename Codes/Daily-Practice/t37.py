class Solution:
    def solveSudoku(self, board: List[List[str]]) -> None:
        """
        Do not return anything, modify board in-place instead.
        """
        num = ['1','2','3','4','5','6','7','8','9']
        map = [[0]*9 for i in range(9)]
        for i in range(9):
            for j in range(9):
                if board[i][j] in num:
                    map[i][j] = int(board[i][j])
        def judge(x:int,y:int,n:int)->bool:
            for i in range(9):
                if map[i][y] == n:
                    return False
                if map[x][i] == n:
                    return False
                xx, yy = 3*(x//3)+i//3, 3*(y//3)+i%3
                if map[xx][yy] == n:
                    return False
            return True
        def dfs(x:int,y:int)->True:
            exist = 0
            for k in range(9):
                if judge(x,y,k+1):
                    map[x][y] = k+1
                    flag = 0
                    exist = 1
                    for i in range(9):
                        if flag:
                            break
                        for j in range(9):
                            if not map[i][j]:
                                flag = 1
                                xn, yn = i,j
                                break
                    if not flag:
                        return True
                    if dfs(xn,yn):
                        return True
                    map[x][y] = 0
            if not exist:
                return False
        ff = 0
        for x in range(9):
            if ff:
                break
            for y in range(9):
                if not map[x][y]:
                    i,j = x,y
                    ff = 1
                    break
        if dfs(i,j):
            for x in range(9):
                for y in range(9):
                    if board[x][y] == ".":
                        board[x][y] = str(map[x][y])