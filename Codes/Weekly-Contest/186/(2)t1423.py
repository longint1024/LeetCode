class Solution:
    def maxScore(self, cardPoints: List[int], k: int) -> int:
        ss = 0
        ans = 0
        n = len(cardPoints)
        cl = [0]*(n+1)
        for i in range(n):
            ss+= cardPoints[i]
            cl[i+1] = ss
        ss, cr = 0, [0]*(n+1)
        for i in range(n-1,-1,-1):
            ss+= cardPoints[i]
            cr[n-i] = ss
        for l in range(k+1):
            r = k-l
            if cl[l]+cr[r]>ans:
                ans = cl[l]+cr[r]
        return ans