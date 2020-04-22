class Solution:
    def isValidSudoku(self, board: List[List[str]]) -> bool:
        m, n = 9, 9
        num = ['1','2','3','4','5','6','7','8','9']
        for i in range(m):
            set1, set2, set3 = set(), set(), set()
            for j in range(n):
                if board[i][j]=='.':
                    pass
                else:
                    if not board[i][j] in num:
                        return False
                    else:
                        if board[i][j] in set1:
                            return False
                        set1.add(board[i][j])
                if board[j][i] == '.':
                    pass
                else:
                    if board[j][i] in set2:
                        return False
                    set2.add(board[j][i])
                x, y = 3*(i//3)+j//3, 3*(i%3)+j%3
                if board[x][y] == '.':
                    pass
                else:
                    if board[x][y] in set3:
                        return False
                    set3.add(board[x][y])
        return True