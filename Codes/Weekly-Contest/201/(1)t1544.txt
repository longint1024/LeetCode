class Solution:
    def makeGood(self, s: str) -> str:
        N = ord('A')-ord('a')
        while 1:
            w = -1
            for i in range(len(s)-1):
                if ord(s[i])+N==ord(s[i+1]) or ord(s[i])-N==ord(s[i+1]):
                    w = i
                    break
            if w == -1:
                break
            else:
                s = s[0:w]+s[w+2:len(s)]
        return s