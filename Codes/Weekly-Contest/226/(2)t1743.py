class Solution:
    def restoreArray(self, adjacentPairs: List[List[int]]) -> List[int]:
        nex = [[] for i in range(200004)]
        n = len(adjacentPairs)
        for p in adjacentPairs:
            nex[p[0]+100000].append(p[1])
            nex[p[1]+100000].append(p[0])
        for i in range(200004):
            if len(nex[i]) == 1:
                b = i
                break
        ans = [b-100000]
        for i in range(n):
            for j in range(2):
                if i==0 or nex[ans[i]+100000][j] != ans[i-1]:
                    t = nex[ans[i]+100000][j]
                    break
            ans.append(t)
        return ans