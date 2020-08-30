class Solution:
    def reverseWords(self, s: str) -> str:
        ans = []
        while 1:
            #print(s)
            index = s.find(" ")
            if index == -1:
                tmp = s
                ans.append(tmp[::-1])
                break
            else:
                tmp = s[0:index]
                s = s[index+1:len(s)]
                ans.append(tmp[::-1])
        return ' '.join(ans)