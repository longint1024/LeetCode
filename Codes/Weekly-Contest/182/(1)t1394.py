class Solution:
    def findLucky(self, arr: List[int]) -> int:
        MAX = 0
        for i in arr:
            if i==arr.count(i) and i>MAX:
                MAX = i
        if MAX > 0:
            return MAX
        else:
            return -1