class Solution:
    def generateParenthesis(self, n: int) -> List[str]:
        ans = []
        if n==0:
            return [""]
        else:
            self.generate(n,n,"",ans)
        return ans
    def generate(self, l: int,r: int,s: str,ss:List[str]):
        if l==0 and r==0:
            ss.append(s)
        if l>0:
            self.generate(l-1,r,s+"(",ss)
        if r>l:
            self.generate(l,r-1,s+")",ss)