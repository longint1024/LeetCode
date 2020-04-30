class Solution:
    ans = 0
    def totalNQueens(self, n: int) -> int:
        map = [[1]*n for i in range(n)]
        self.ans = 0
        def sweep(r:int,c:int,e:int)->None:
            for i in range(n):
                map[i][c] -= e
                if r+c-i>=0 and r+c-i<n:
                    map[i][r+c-i] -= e
                if i-r+c>=0 and i-r+c<n:
                    map[i][i-r+c] -= e
        def dfs(r:int)->None:
            for c in range(n):
                if map[r][c]==1:
                    if r == n-1:
                        self.ans += 1
                        return
                    sweep(r,c,1)
                    dfs(r+1)
                    sweep(r,c,-1)
            return
        dfs(0)
        return self.ans