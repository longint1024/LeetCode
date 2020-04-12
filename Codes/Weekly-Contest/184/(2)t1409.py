class Solution:
    def processQueries(self, queries: List[int], m: int) -> List[int]:
        p = []
        ans = []
        for i in range(m):
            p.append(i+1)
        for i in queries:
            for j in range(len(p)):
                if i == p[j]:
                    p.remove(i)
                    p = [i]+p
                    ans.append(j)
                    break
        return ans