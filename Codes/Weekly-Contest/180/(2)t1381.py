class CustomStack:
    stack = []
    MAX = 0
    
    def __init__(self, maxSize: int):
        self.MAX = maxSize
        self.stack = []

    def push(self, x: int) -> None:
        if len(self.stack)<self.MAX:
            self.stack.append(x)

    def pop(self) -> int:
        if self.stack == []:
            return -1
        else:
            ans = self.stack[len(self.stack)-1]
            del self.stack[len(self.stack)-1]
            return ans

    def increment(self, k: int, val: int) -> None:
        if len(self.stack)<k:
            for i in range(len(self.stack)):
                self.stack[i] += val
        else:
            for i in range(k):
                self.stack[i]+=val


# Your CustomStack object will be instantiated and called as such:
# obj = CustomStack(maxSize)
# obj.push(x)
# param_2 = obj.pop()
# obj.increment(k,val)