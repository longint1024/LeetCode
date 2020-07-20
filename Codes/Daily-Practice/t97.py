class Solution:
    def isInterleave(self, s1: str, s2: str, s3: str) -> bool:
        if len(s1)<len(s2):
            s1, s2 = s2, s1
        n1, n2, n3 = len(s1), len(s2), len(s3)
        if n3 != n1+n2:
            return False
        dp = [0 for i in range(n2+1)]
        dp[0] = 1
        for j in range(1,n2+1):
            if s2[j-1] == s3[j-1]:
                dp[j] = 1
            else:
                break
        for i in range(1,n1+1):
            for j in range(n2+1):
                k = i+j
                dp[j] =  (i>0 and dp[j] and s1[i-1] == s3[k-1]) or (j>0 and dp[j-1] and s2[j-1] == s3[k-1])
        return bool(dp[n2])