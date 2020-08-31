class Solution:
    def canVisitAllRooms(self, rooms: List[List[int]]) -> bool:
        n = len(rooms)
        havebeen, tot, queue = [0 for _ in range(n)], 1, [0]
        havebeen[0] = 1
        while queue:
            before = tot
            tmp = queue.pop(0)
            for i in rooms[tmp]:
                if not havebeen[i]:
                    queue.append(i)
                    havebeen[i] = 1
                    before += 1
            tot = before
            #print(tot)
        return tot == n