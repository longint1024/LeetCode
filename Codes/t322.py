class Solution:
    coins = []
    n = 0
    ans = []
    def coinChange(self, coins: List[int], amount: int) -> int:
        if amount == 0:
            return 0
        coins.sort(reverse=True)
        self.coins = coins
        self.n = 0
        MAX = amount//min(coins)+1
        self.ans = MAX
        self.DFS(amount, 0, 0)
        if self.ans<MAX:
            return self.ans
        else:
            return -1
    def DFS(self, res, step, index) -> None:
        if index>len(self.coins)-1:
            return
        for i in self.coins[index:len(self.coins)]:
            if res % self.coins[index]==0:
                if step+res//self.coins[index]<self.ans:
                    self.ans = step+res//self.coins[index]
                return
        if (self.ans-step)*self.coins[index]<res:
            return
        for j in range(res//self.coins[index],-1,-1):
            self.DFS(res-j*self.coins[index], step+j,index+1)
        return