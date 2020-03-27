class Solution:
    ans=[]
    cand=[]
    n=0
    def combinationSum(self, candidates: List[int], target: int) -> List[List[int]]:
        if candidates==[]:
            return []
        self.ans=[]
        candidates.sort()
        self.cand = candidates
        self.n=len(self.cand)
        self.com(0, target, [])
        return self.ans
    def com(self, index:int, target: int, newans: List[int]) -> None:
        if target<self.cand[index]:
            return
        for i in range(index, self.n):
            if self.cand[i]==target:
                self.ans.append(newans+[target])
        for i in range(index,self.n):
            tmp = self.cand[i]
            self.com(i, target-tmp, newans+[tmp])