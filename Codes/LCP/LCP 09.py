class Solution:
    def minJump(self, jump: List[int]) -> int:
        N = len(jump)
        get = [jump[i]+i for i in range(len(jump))]
        queue = [[0,0]]
        front, rear = -1,0
        dao = [0 for i in range(N)]
        dao[0] =1
        MAX = 0
        while front<rear:
            front += 1
            x = queue[front][0]
            step = queue[front][1]
            for i in range(MAX,x):
                if dao[i]==0:
                    rear += 1
                    queue.append([i,step+1])
                    dao[i] = 1
            if x+1 > MAX:
                MAX = x+1
            if get[x]>N-1:
                return step+1
            if not dao[get[x]]:
                rear += 1
                queue.append([get[x],step+1])
                dao[get[x]] = 1
        