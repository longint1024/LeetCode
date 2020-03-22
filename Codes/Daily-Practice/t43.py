class Solution:
    def multiply(self, num1: str, num2: str) -> str:
        if num1 == '0' or num2 =='0':
            return '0'
        def chr2num(c:chr)->int:
            return ord(c)-ord('0')
        len1, len2 = len(num1), len(num2)
        ans = [0 for i in range(len1+len2)]
        for i in range(len1):
            for j in range(len2):
                ans[i+j] += chr2num(num1[len1-i-1])*chr2num(num2[len2-j-1])
        for i in range(len1+len2):
            if ans[i]>=10:
                ans[i+1]+=ans[i]//10
                ans[i] = ans[i]%10
        ans.reverse()
        if ans[0]==0:
            ans.remove(ans[0])
        for i in range(len(ans)):
            ans[i] = chr(ans[i]+48)
        return "".join(ans)
            