class Solution:
    def isMatch(self, s: str, p: str) -> bool:
        return ismatching(s,p)
def ismatching(s: str, p: str) -> bool:
    lens=len(s)
    lenp=len(p)
    if lenp==0:
        return lens==0
    if lenp==1:
        return (lens==1) and (p[0]==s[0] or p[0]=='.')
    if p[1]!="*":
        if lens==0:
            return 0
        else:
            return (s[0]==p[0] or p[0]==".") and (ismatching(s[1:lens],p[1:lenp]))
    else:
        while(len(s)>0 and (p[0]==s[0] or p[0]==".")):
            if ismatching(s,p[2:lenp]):
                return 1
            s=s[1:len(s)]
        return (ismatching(s,p[2:lenp]))