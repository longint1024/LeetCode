class Solution:
    ans=set()
    cand=()
    n=0
    def combinationSum2(self, candidates: List[int], target: int) -> List[List[int]]:
        if candidates==[]:
            return []
        self.ans=set()
        candidates.sort()
        self.cand = candidates
        self.n=len(self.cand)
        self.com(-1, target, [])
        return list(self.ans)
    def com(self, index:int, target: int, newans: List[int]) -> None:
        if index!=-1 and target<self.cand[index]:
            return
        for i in range(index+1, self.n):
            if self.cand[i]==target:
                self.ans.add(tuple(newans+[target]))
        for i in range(index+1,self.n):
            tmp = self.cand[i]
            self.com(i, target-tmp, newans+[tmp])