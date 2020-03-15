class Solution:
    def canThreePartsEqualSum(self, A: List[int]) -> bool:
        ss = sum(A)
        if ss%3 != 0:
            return False
        else:
            t = ss//3
            tot = 0
            flag1 = 0
            flag2 = 0
            index1 = -1
            index2 = -1
            for i in range(len(A)-1):
                tot = tot+A[i]
                if tot == t and not flag1:
                    flag1 = 1
                    continue
                if tot == 2*t and flag1 and not flag2:
                    flag2 = 1
                    continue
            if flag1 and flag2:
                return True
            return False