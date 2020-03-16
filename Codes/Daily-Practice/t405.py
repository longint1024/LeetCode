class Solution:
    def toHex(self, num: int) -> str:
        if(num==0):
            return "0"
        else:
            s=['0','1','2','3','4','5','6','7','8','9','a','b','c','d','e','f']
            ans=""
            for i in range(8):
                ans=s[num&15]+ans
                num=num>>4
            ans=ans.lstrip('0')
            return ans