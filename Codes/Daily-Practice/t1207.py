class Solution:
    def uniqueOccurrences(self, arr: List[int]) -> bool:
        num = {}
        for i in arr:
            if i not in num:
                num[i] = 1
            else:
                num[i] += 1
        numofshow = set()
        for i in num:
            if num[i] in numofshow:
                return False
            numofshow.add(num[i])
        return True