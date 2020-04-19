class Solution:
    def reformat(self, s: str) -> str:
        number = ['0','1','2','3','4','5','6','7','8','9']
        n, c = [], []
        for i in s:
            if i in number:
                n.append(i)
            else:
                c.append(i)
        ans = []
        indexn = 0
        indexc = 0
        if len(n)-len(c)==1:
            ans.append(n[indexn])
            indexn+=1
            while 1:
                if indexn>len(n)-1:
                    break
                ans.append(c[indexc])
                ans.append(n[indexn])
                indexc+=1
                indexn+=1
            return ''.join(ans)
        if len(c)-len(n)==1:
            ans.append(c[indexc])
            indexc+=1
            while 1:
                if indexn>len(n)-1:
                    break
                ans.append(n[indexn])
                ans.append(c[indexc])
                indexc+=1
                indexn+=1
            return ''.join(ans)
        if len(c)==len(n):
            while 1:
                ans.append(n[indexn])
                ans.append(c[indexc])
                indexc+=1
                indexn+=1
                if indexn>len(n)-1:
                    break
            return ''.join(ans)
        return ''