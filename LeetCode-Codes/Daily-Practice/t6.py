class Solution:
    def convert(self, s: str, numRows: int) -> str:
        if(numRows==1 or numRows>len(s)):
            return s
        ans, index, step = ['' for i in range(numRows)], 0, 1
        for char in s:
            ans[index]=ans[index]+char
            if(index==numRows-1):
                step = -1
            if(index==0):
                step = 1
            index = index + step
        ans = ''.join(ans)
        return ans