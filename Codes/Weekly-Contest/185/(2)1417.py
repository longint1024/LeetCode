class Solution:
    def displayTable(self, orders: List[List[str]]) -> List[List[str]]:
        food = set()
        table = set()
        for i in orders:
            food.add(i[2])
            table.add(int(i[1]))
        food = list(food)
        food.sort()
        table = list(table)
        table.sort()
        tt = [0 for i in range(504)]
        for i in range(len(table)):
            tt[table[i]] = i
            
        ans = [[0 for i in range(1+len(food))]for j in range(1+len(table))]
        ans[0][0] = 'Table'
        for i in range(len(food)):
            ans[0][i+1] = food[i]
        for i in range(len(table)):
            ans[i+1][0] = table[i]
            
        for i in orders:
            t = tt[int(i[1])]
            for j in range(len(food)):
                if food[j] == i[2]:
                    f = j
                    break
            ans[t+1][f+1]+=1
        for i in range(1+len(table)):
            for j in range(1+len(food)):
                ans[i][j] = str(ans[i][j])
        return ans