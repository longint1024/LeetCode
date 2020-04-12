class UndergroundSystem:
    ft = []
    ins = []
    def __init__(self):
        self.ft = []
        self.ins = []

    def checkIn(self, id: int, stationName: str, t: int) -> None:
        self.ins.append([id,stationName,t])

    def checkOut(self, id: int, stationName: str, t: int) -> None:
        for i in self.ins:
            if i[0] == id:
                index = i
        self.ft.append([index[1],stationName,t-index[2]])
        self.ins.remove(index)
                

    def getAverageTime(self, startStation: str, endStation: str) -> float:
        ans = 0.0
        n = 0
        for i in self.ft:
            if i[0]==startStation and i[1]==endStation:
                ans += i[2]
                n += 1
        return float(ans/n)


# Your UndergroundSystem object will be instantiated and called as such:
# obj = UndergroundSystem()
# obj.checkIn(id,stationName,t)
# obj.checkOut(id,stationName,t)
# param_3 = obj.getAverageTime(startStation,endStation)