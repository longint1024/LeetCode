class Solution:
    def maxScore(self, s: str) -> int:
        MAX = -1
        for i in range(len(s)-1):
            left = s[0:i+1]
            right = s[i+1:len(s)]
            score = left.count('0')+right.count('1')
            if score>MAX:
                MAX = score
        return MAX