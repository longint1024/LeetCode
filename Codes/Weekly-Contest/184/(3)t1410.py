class Solution:
    def entityParser(self, text: str) -> str:
        ans = ''
        ll = [5,5,4,3,3,6]
        ss = ['quot;','apos;','amp;','gt;','lt;','frasl;']
        a = ['"',"'",'&','>','<','/']
        i = 0
        while i<len(text):
            if text[i] == '&':
                flag = 0
                for j in range(6):
                    if i+ll[j]<len(text) and text[i+1:i+ll[j]+1] == ss[j]:
                        ans = ans+a[j]
                        i = i+ll[j]+1
                        flag = 1
                        break
                if flag:
                    continue
            ans = ans+text[i]
            i = i+1
        return ans