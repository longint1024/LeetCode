class Solution:
    def countAndSay(self, n: int) -> str:
        ans = [''for i in range(30)]
        ans[0]='1'
        for i in range(1,n):
            ans[i]=self.count(ans[i-1])
        return ans[n-1]
    def count(self,s: str) -> str:
        theans = ""
        lens = len(s)
        num = []
        cnt = []
        index = -1
        for i in range(lens):
            if index == -1 or s[i]!=num[index]:
                num.append(s[i])
                index = index+1
                cnt.append(1)
            else:
                cnt[index]=cnt[index]+1
        for i in range(index+1):
            theans = theans + str(cnt[i]) + num[i]
        return theans