class Solution:
    def flipAndInvertImage(self, A: List[List[int]]) -> List[List[int]]:
        for l in A:
            l=l.reverse()
        for l in A:
            for i in range(len(l)):
                l[i]=l[i]^1
        return A
            