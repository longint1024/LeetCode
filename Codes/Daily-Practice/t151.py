class Solution:
    def reverseWords(self, s: str) -> str:
        s = s.split()
        ans = []
        for i in range(len(s)):
            tmp = s[len(s)-i-1]
            ans.append(tmp)
        s = ' '.join(ans)
        return s