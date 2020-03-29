class Solution:
    def numRookCaptures(self, board: List[List[str]]) -> int:
        def suit(x:int,y:int)->bool:
            if x>7 or y>7 or x<0 or y<0:
                return 0
            return 1
        def find(x:int ,y:int)->int:
            ans = 0
            dirx,diry = [-1,1,0,0], [0,0,1,-1]
            for i in range(4):
                xx = x+dirx[i]
                yy = y+diry[i]
                while suit(xx,yy):
                    if board[xx][yy] == 'B':
                        break
                    if board[xx][yy] == 'p':
                        ans += 1
                        break
                    xx = xx+dirx[i]
                    yy = yy+diry[i]
            return ans
        for i in range(8):
            for j in range(8):
                if board[i][j] == 'R':
                    index_i = i
                    index_j = j
                    break
        return find(index_i,index_j)