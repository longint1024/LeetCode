class Solution:
    def addBinary(self, a: str, b: str) -> str:
        len1, len2 = len(a), len(b)
        ll = max(len1,len2)
        c = ''
        carry = 0
        def num(i:int, t:int)->int:
            if t:
                if i>len2-1:
                    return 0
                return 1 if b[len2-1-i]=='1' else 0
            else:
                if i>len1-1:
                    return 0
                return 1 if a[len1-1-i]=='1' else 0
        for i in range(ll):
            tmp = carry+num(i,0)+num(i,1)
            if tmp>1:
                tmp -= 2
                carry = 1
            else:
                carry = 0
            c = str(tmp) + c
        if carry:
            return '1'+c
        else:
            return c      