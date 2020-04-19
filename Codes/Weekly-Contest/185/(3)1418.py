class Solution:
    def minNumberOfFrogs(self, croakOfFrogs: str) -> int:
        f = ['c','r','o','a','k']
        num = [0 for i in range(5)]
        MIN = 0
        for i in croakOfFrogs:
            if not (i in f):
                return -1
            for p in range(len(f)):
                if f[p] == i:
                    k = p
                    break
            for j in range(k):
                if num[j] <num[k]:
                    return -1
            num[k]+=1
            if k==4:
                for j in range(5):
                    num[j]-=1
            for j in range(5):
                if num[j]>MIN:
                    MIN = num[j]
        for i in range(5):
            for j in range(i):
                if num[j]!=num[i]:
                    return -1
        return MIN