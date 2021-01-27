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
    def maxNumEdgesToRemove(self, n: int, edges: List[List[int]]) -> int:
        ufa, ufb, ans = UnionFind(n), UnionFind(n), 0
        for e in edges:
            e[1],e[2] = e[1]-1,e[2]-1
            if e[0] == 3:
                if ufa.connected(e[1],e[2]):
                    ans += 1
                else:
                    ufa.unite(e[1],e[2])
                    ufb.unite(e[1],e[2])
        for e in edges:
            if e[0] == 1:
                if ufa.connected(e[1],e[2]):
                    ans += 1
                else:
                    ufa.unite(e[1],e[2])
            elif e[0] == 2:
                if ufb.connected(e[1],e[2]):
                    ans += 1
                else:
                    ufb.unite(e[1],e[2])
        if ufa.setCount == 1 and ufb.setCount == 1:
            return ans
        return -1