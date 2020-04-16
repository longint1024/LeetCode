class Solution:
    def plusOne(self, digits: List[int]) -> List[int]:
        n = len(digits)-1
        digits[n] += 1
        while n>0:
            n = n-1
            if digits[n+1]<10:
                break
            else:
                digits[n] += 1
                digits[n+1] = 0
        if digits[0]==10:
            return [1,0]+digits[1:len(digits)]
        return digits