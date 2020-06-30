class CQueue:

    def __init__(self):
        self.qin = []
        self.qout = []
        
    def appendTail(self, value: int) -> None:
        self.qin.append(value)

    def deleteHead(self) -> int:
        if self.qout:
            return self.qout.pop()
        else:
            if self.qin:
                while self.qin:
                    self.qout.append(self.qin.pop())
                return self.qout.pop()
            else:
                return -1


# Your CQueue object will be instantiated and called as such:
# obj = CQueue()
# obj.appendTail(value)
# param_2 = obj.deleteHead()