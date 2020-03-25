class Solution:
    def replaceSpace(self, s: str) -> str:
        ans = ''
        for i in s:
            if i != ' ':
                ans += i
            else:
                ans += '%20'
        return ans