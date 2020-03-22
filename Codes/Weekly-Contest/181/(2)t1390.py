class Solution:
    def sumFourDivisors(self, nums: List[int]) -> int:
        def prime(x:int) -> int:
            if x<6:
                return 0
            a = int(x**0.5)
            if a*a == x:
                return 0
            flag = 0
            for i in range(2,a+1):
                if flag and x%i == 0:
                    return 0
                if x%i == 0 and not flag:
                    flag = 1
                    p = i
            if flag:
                return(1+x+p+x//p)
            else:
                return 0
        ans = 0
        for i in nums:
            ans += prime(i)
        return ans