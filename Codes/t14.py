class Solution:
    def longestCommonPrefix(self, strs: List[str]) -> str:
        num = len(strs)
        if num==0:
            return ''
        minlen = 2147483647
        index = 0
        for i in range(num):
            ll = len(strs[i])
            if ll<minlen:
                minlen=ll
                index=i
        flag=1
        for i in range(minlen):
            for j in range(num):
                if strs[index][i]!=strs[j][i]:
                    flag=0
                    break
            if not flag:
                break
        print(i)
        if flag:
            return strs[index]
        else:
            return strs[index][0:i]