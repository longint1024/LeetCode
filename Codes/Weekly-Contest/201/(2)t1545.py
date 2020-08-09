class Solution:
    def findKthBit(self, n: int, k: int) -> str:
        s = "0"
        for i in range(n-1):
            tmp = ""
            for j in range(len(s)-1,-1,-1):
                if s[j] == '0':
                    tmp += '1'
                else:
                    tmp += '0'
            s = s+"1"
            s = s+tmp
        return s[k-1]