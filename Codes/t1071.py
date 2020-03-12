class Solution:
    def gcdOfStrings(self, str1: str, str2: str) -> str:
        if str1+str2 != str2+str1:
            return ''
        def gcd(a:int,b:int) -> int:
            return gcd(b,a%b) if b else a
        len1, len2 = len(str1), len(str2)
        lenc = gcd(len1,len2)
        return str1[0:lenc]