class Solution:
    def countCharacters(self, words: List[str], chars: str) -> int:
        count = [0 for i in range(26)]
        ans = 0
        for i in chars:
            count[ord(i)-ord('a')] += 1
        for i in words:
            tmp = [count[i] for i in range(26)]
            flag = 1
            for j in i:
                if tmp[ord(j)-ord('a')]>0:
                    tmp[ord(j)-ord('a')] -= 1
                else:
                    flag = 0
                    break
            if flag:
                ans += len(i)
        return ans