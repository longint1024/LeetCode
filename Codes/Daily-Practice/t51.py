class Solution:
    def solveNQueens(self, n: int) -> List[List[str]]:
        map = [[0]*n for i in range(n)]
        ans = []
        def trans(b:List[List[int]]) ->List[List[str]]:
            solution = []
            for i in range(n):
                tmp = ''
                for j in range(n):
                    if map[i][j]:
                        tmp += 'Q'
                    else:
                        tmp += '.'
                solution.append(tmp)
            return solution
        def judge(x:int,y:int)->bool:
            for i in range(n):
                if map[i][y]:
                    return False
            for xx in range(max(0,x+y-n+1),min(x+y+1,n)):
                yy = x+y-xx
                if map[xx][yy]:
                    return False
            for xx in range(max(0,x-y),min(x-y+n,n)):
                yy = xx-x+y
                if map[xx][yy]:
                    return False
            return True
        def dfs(r:int)->None:
            for c in range(n):
                if judge(r,c):
                    map[r][c] = 1
                    if r==n-1:
                        ans.append(trans(map))
                        map[r][c] = 0
                        return
                    dfs(r+1)
                    map[r][c] = 0
        dfs(0)
        return ans