# 并查集模板
class UnionFind:
    def __init__(self, n: int):
        self.parent = list(range(n))
        self.size = [1] * n
        self.n = n
        # 当前连通分量数目
        self.setCount = n
    
    def findset(self, x: int) -> int:
        if self.parent[x] == x:
            return x
        self.parent[x] = self.findset(self.parent[x])
        return self.parent[x]
    
    def unite(self, x: int, y: int) -> bool:
        x, y = self.findset(x), self.findset(y)
        if x == y:
            return False
        if self.size[x] < self.size[y]:
            x, y = y, x
        self.parent[y] = x
        self.size[x] += self.size[y]
        self.setCount -= 1
        return True
    
    def connected(self, x: int, y: int) -> bool:
        x, y = self.findset(x), self.findset(y)
        return x == y
class Solution:
    def numSimilarGroups(self, strs: List[str]) -> int:
        def judge(s1,s2):
            count = 0
            for i in range(len(s1)):
                if s1[i]!=s2[i]:
                    count += 1
                if  count>2:
                    break
            return count == 0 or count == 2
        n = len(strs)
        uf = UnionFind(n)
        for i in range(n):
            for j in range(n):
                if i!=j and judge(strs[i],strs[j]):
                    uf.unite(i,j)
        return uf.setCount
                    