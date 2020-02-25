class Solution:
    def myAtoi(self, str: str) -> int:
        number = '0123456789'
        ans = ''
        flag = 1
        MAX = 2147483647
        MIN = -2147483648
        str = str.lstrip()
        if(str==''):
            return 0
        c = 1
        if str[0] in ("+","-"):
            if str[0]=="-":
                c = -1
            str = str[1:len(str)]
        for char in str:
            if(char in number):
                ans=ans+char
            else:
                break
        if(ans==''):
            return 0
        ans = c*int(ans)
        if(ans>MAX):
            return MAX
        if(ans<MIN):
            return MIN
        return ans