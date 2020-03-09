class Solution:
    def numTimesAllBlue(self, light: List[int]) -> int:
        ans = 0
        on = set()
        maxon = 0
        maxnow  = 0
        for i in light:
            if i>maxnow:
                maxnow = i
            on.add(i)
            flag = 1
            while (maxon+1) in on:
                maxon = maxon + 1
            if maxnow == maxon:
                ans = ans+1
        return ans