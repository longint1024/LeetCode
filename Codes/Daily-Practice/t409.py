class Solution:
    def longestPalindrome(self, s: str) -> int:
        big = [0 for i in range(26)]
        small = [0 for i in range(26)]
        for i in s:
            if ord(i)>=ord('a'):
                small[ord(i)-ord('a')] += 1
            else:
                big[ord(i)-ord('A')] += 1
        SUM = 0
        count_odd = 0
        for i in range(26):
            if big[i] & 1 == 1:
                count_odd += 1
            SUM += big[i]
            if small[i] & 1 == 1:
                count_odd += 1
            SUM += small[i]
        if count_odd == 0:
            return SUM
        else:
            return SUM - count_odd + 1
                