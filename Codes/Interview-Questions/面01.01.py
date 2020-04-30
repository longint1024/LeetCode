class Solution:
    def isUnique(self, astr: str) -> bool:
        s = list(astr)
        ss = set(s)
        if len(ss)==len(s):
            return True
        else:
            return False