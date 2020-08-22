class Solution:
    def judgePoint24(self, nums: List[int]) -> bool:
        def compute(num:List[int])-> bool:
            n = len(num)
            if n == 1:
                return abs(num[0]-24)<0.000001
            for i in range(n-1):
                for j in range(i+1,n):
                    new = []
                    for k in range(n):
                        if k!=i and k!=j:
                            new.append(num[k])
                    a, b = num[i], num[j]
                    for t in range(6):
                        if t == 0:
                            new.append(a+b)
                            if compute(new):
                                return True
                        elif t == 1:
                            new.append(a*b)
                            if compute(new):
                                return True
                        elif t == 2:
                            if b == 0:
                                continue
                            new.append(a/b)
                            if compute(new):
                                return True
                        elif t == 3:
                            if a == 0:
                                continue
                            new.append(b/a)
                            if compute(new):
                                return True
                        elif t == 4:
                            new.append(a-b)
                            if compute(new):
                                return True
                        elif t == 5:
                            new.append(b-a)
                            if compute(new):
                                return True
                        new.pop()
            return False
        return compute(nums)