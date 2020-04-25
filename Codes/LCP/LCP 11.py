class Solution:
    def expectNumber(self, scores: List[int]) -> int:
        ans = 1
        scores.sort()
        for i in range(1,len(scores)):
            if scores[i]==scores[i-1]:
                pass
            else:
                ans+=1
        return ans