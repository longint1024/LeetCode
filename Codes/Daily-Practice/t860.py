class Solution:
    def lemonadeChange(self, bills: List[int]) -> bool:
        n5, n10 = 0, 0
        for i in bills:
            if i == 5:
                n5 += 1
            elif i == 10:
                if n5 == 0:
                    return False
                else:
                    n5 -= 1
                    n10 += 1
            elif i == 20:
                if n10 > 0:
                    if n5 > 0:
                        n10 -= 1
                        n5 -= 1
                    else:
                        return False
                else:
                    if n5 > 3:
                        n5 -= 3
                    else:
                        return False
        return True