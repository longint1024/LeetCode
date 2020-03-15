class Solution:
    def letterCombinations(self, digits: str) -> List[str]:
        if digits=="":
            return []
        number = ['abc','def','ghi','jkl','mno','pqrs','tuv','wxyz']
        lend = len(digits)
        ans =  ['']
        for i in range(lend):
            letter = number[int(digits[i])-2]
            lenl = len(letter)
            lena = len(ans)
            for j in range(lena):
                for k in range(lenl):
                    ans.append(ans[j]+letter[k])
            ans = ans[lena:len(ans)]
        return ans