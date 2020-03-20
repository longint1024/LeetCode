from queue import PriorityQueue
class Solution:
    def getLeastNumbers(self, arr: List[int], k: int) -> List[int]:
        k_heap = PriorityQueue()
        arr = [-arr[i] for i in range(len(arr))]
        for i in range(len(arr)):
            k_heap.put(arr[i])
            if k_heap.qsize()>k:
                tmp = k_heap.get()
        ans = [-k_heap.get() for i in range(k)]
        return ans