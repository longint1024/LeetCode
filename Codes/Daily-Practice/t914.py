class Solution:
    def hasGroupsSizeX(self, deck: List[int]) -> bool:
        def gcd(a:int, b:int)->int:
            return a if b==0 else gcd(b,a%b)
        vals = collections.Counter(deck).values()
        return reduce(gcd, vals) >= 2        