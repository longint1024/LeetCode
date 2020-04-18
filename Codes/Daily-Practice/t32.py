class Solution:
    def longestValidParentheses(self, s: str) -> int:
        n = len(s)
        dp = [0 for i in range(n)]
        MAX = 0
        for i in range(n):
            if s[i] == '(':
                continue
            if i>0 and s[i-1]=='(':
                dp[i] = dp[i-2]+2
            if s[i-1]==')':
                if i-dp[i-1]-1>=0 and s[i-dp[i-1]-1] == '(':
                    dp[i] = dp[i-1]+2
                    if i-dp[i-1]-1>0:
                        dp[i] += dp[i-dp[i-1]-2]
            if dp[i]>MAX:
                    MAX = dp[i]
        return MAX  