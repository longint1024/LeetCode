class Solution:
    def compressString(self, S: str) -> str:
        index = 0
        n = len(S)
        ans = ''
        while 1:
            if index>n-1:
                break
            count = 1
            while index<n-1 and S[index+1]==S[index]:
                index = index+1
                count +=1
            ans = ans+S[index]+str(count)
            index +=1
        if len(ans)>=n:
            return S
        else:
            return ans