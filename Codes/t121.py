class Solution:
    def maxProfit(self, prices: List[int]) -> int:
        if prices == []:
            return 0
        n = len(prices)
        MAX = [0 for i in range(n)]
        MAX[n-1] = prices[n-1]
        for i in range(n-2,0,-1):
            if prices[i]>MAX[i+1]:
                MAX[i] = prices[i]
            else:
                MAX[i] = MAX[i+1]
        ans = 0
        for i in range(n-1):
            if MAX[i+1]-prices[i]>ans:
                ans = MAX[i+1]-prices[i]
        return ans