class Solution:
    def groupAnagrams(self, strs: List[str]) -> List[List[str]]:
        n = len(strs)
        index = [1 for i in range(n)]
        for i in range(n):
            for j in range(len(strs[i])):
                index[i] = index[i]*(ord(strs[i][j])+101)
        kind = set()
        for i in range(n):
            kind.add(index[i])
        nk = len(kind)
        kind = list(kind)
        ans = [[] for i in range(nk)]
        for i in range(nk):
            for j in range(n):
                if index[j] == kind[i]:
                    ans[i].append(strs[j])
        return ans