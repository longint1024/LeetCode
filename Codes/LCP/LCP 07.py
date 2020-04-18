class Solution:
    def numWays(self, n: int, relation: List[List[int]], k: int) -> int:
        queue = [0]
        front = -1
        rear = 0
        for ss in range(k):
            tmp = []
            for x in queue:
                for i in range(n):
                    if [x,i] in relation:
                        tmp.append(i)
            queue = tmp
        ans = 0
        for i in queue:
            if i==n-1:
                ans += 1
        return ans