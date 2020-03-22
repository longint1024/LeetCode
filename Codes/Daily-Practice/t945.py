class Solution:
    def minIncrementForUnique(self, A: List[int]) -> int:
        count = [0 for i in range(80004)]
        for i in A:
            count[i] += 1
        move = 0
        for i in range(len(count)):
            if count[i]>1:
                count[i+1] += count[i] - 1
                move += count[i] - 1
        return move