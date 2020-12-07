class Solution:
    def matrixScore(self, A: List[List[int]]) -> int:
        w, ans = 1, 0
        m, n = len(A), len(A[0])
        for j in range(n-1,0,-1):
            s = 0
            for i in range(m):
                s += not(A[i][0]^A[i][j])
            s = max(s,m-s)
            ans += w*s
            w = w*2
        return (ans+w*m)