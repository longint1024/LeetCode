from queue import PriorityQueue
class Solution:
    def maxPerformance(self, n: int, speed: List[int], efficiency: List[int], k: int) -> int:
        items = [(speed[i], efficiency[i]) for i in range(n)]
        items.sort(key=lambda item:item[1], reverse=True)
        add_sum = 0
        pq = PriorityQueue()
        res = 0
        for i in range(n):
            pq.put(items[i][0])
            add_sum += items[i][0]
            if pq.qsize() > k:
                add_sum -= pq.get()
            val = add_sum * items[i][1]
            if val > res:
                res = val
        return res % (10 ** 9 + 7)