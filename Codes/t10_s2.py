class Solution:
    def isMatch(self, s: str, p: str) -> bool:
        lens, lenp = len(s), len(p)
        if lenp == 0 and lens!=0:
            return 0
        if lenp ==0 and lens ==0:
            return 1
        dp = [[0]*(lenp+1) for i in range(lens+1)]  #机智预留空间，防止有测试点s是空的来坑爸爸我
        dp[0][0]=1
        if lens>0:
            dp[1][1]=(s[lens-1]==p[lenp-1] or p[lenp-1]=='.')
        i = 0
        for i in range(lens+1):
            for j in range(2,lenp+1):
                if p[lenp-j+1]!="*":
                    if i==0:
                        dp[i][j]=0
                    else:
                        if ((s[lens-i]==p[lenp-j]) or (p[lenp-j]==".")) and (dp[i-1][j-1]):
                            dp[i][j]=1
                else:
                    if i==0:
                        if dp[i][j-2]:
                            dp[i][j]=1
                    else:
                        flag=0
                        if dp[i][j-2]:
                            dp[i][j]=1
                            flag=1
                        k=i
                        while (k>0 and not flag):
                            if ((s[lens-k]==p[lenp-j]) or (p[lenp-j]=='.')):
                                if (dp[k-1][j-2]):
                                    dp[i][j]=1
                                    break
                                k = k-1
                            else:
                                break
        print(dp)
        return dp[lens][lenp]