class Solution:
    def countSubTrees(self, n: int, edges: List[List[int]], labels: str) -> List[int]:
        tree = [[] for i in range(n)]
        show = [0 for i in range(n)]
        show[0] = 1
        for i in range(n-1):
            if not show[edges[i][1]]:
                tree[edges[i][0]].append(edges[i][1])
                show[edges[i][1]] = 1
            else:
                tree[edges[i][1]].append(edges[i][0])
                show[edges[i][0]] = 1
        la = [[0 for i in range(26)]for j in range(n)]
        ceng = [[0]]
        while 1:
            tmp = []
            for i in ceng[len(ceng)-1]:
                for j in tree[i]:
                    tmp.append(j)
            if tmp == []:
                break
            ceng.append(tmp)
        for i in range(len(ceng)-1,-1,-1):
            for j in ceng[i]:
                for k in tree[j]:
                    for p in range(26):
                        la[j][p]+=la[k][p]
                    la[j][ord(labels[k])-ord('a')] += 1
        ans = [1 for i in range(n)]
        for i in range(n):
            ans[i] += la[i][ord(labels[i])-ord('a')]
        return ans
                