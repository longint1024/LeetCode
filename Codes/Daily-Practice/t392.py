class Solution:
    def isSubsequence(self, s: str, t: str) -> bool:
        k, n = 0, len(t)
        if n<len(s):
            return False
        if t=="":
            return s==""
        for i in s:
            if k>n-1:
                return False
            while t[k]!=i:
                k += 1
                if k>n-1:
                    return False
            k+=1
        return True