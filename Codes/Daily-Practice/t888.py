class Solution:
    def fairCandySwap(self, A: List[int], B: List[int]) -> List[int]:
        dif = (sum(B) - sum(A))//2
        B = set(B)
        for i in A:
            if i+dif in B:
                return [i,i+dif]