class Solution:
    def longestPrefix(self, s: str) -> str:
        next = [0 for i in range(len(s)+1)]
        def getnext(s:str) ->None:
            n = len(s)
            next[0] = 0
            i = 0
            for j in range(1,len(s)):
                while(s[i]!=s[j] and i>0):
                    i = next[i-1]
                if (s[i]==s[j]):
                    i += 1
                    next[j] = i
                else:
                    next[j] = 0
        getnext(s)
        return s[0:next[len(s)-1]]