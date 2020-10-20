class Solution:
    def backspaceCompare(self, S: str, T: str) -> bool:
        s,t = [], []
        for c in S:
            if c!='#':
                s.append(c)
            elif s:
                s.pop()
        for c in T:
            if c!='#':
                t.append(c)
            elif t:
                t.pop()
        return s==t