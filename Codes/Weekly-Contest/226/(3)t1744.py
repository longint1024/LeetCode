class Solution:
    def canEat(self, candiesCount: List[int], queries: List[List[int]]) -> List[bool]:
        n = len(candiesCount)
        s = [0 for i in range(n)]
        s[0] = candiesCount[0]
        for i in range(1,n):
            s[i]  = s[i-1] + candiesCount[i]
        ans = []
        for f,d,m in queries:
            if d>=s[f]:
                ans.append(False)
                continue
            if f == 0:
                ans.append(True)
                continue
            if m*(d+1)<=s[f-1]:
                ans.append(False)
                continue
            ans.append(True)
        return ans