from queue import PriorityQueue
class Solution:
    def getLeastNumbers(self, arr: List[int], k: int) -> List[int]:
        count = [0 for i in range(10001)]
        MAX = 0
        for i in arr:
            count[i] += 1
            if i>MAX:
                MAX = i
        num = 0
        ans = []
        print(count[0:MAX+1])
        for i in range(MAX+1):
            if not count[i]:
                continue
            num += count[i]
            if num<=k:
                for j in range(count[i]):
                    ans.append(i)
            if num>k:
                for j in range(k-num+count[i]):
                    ans.append(i)
                break
        return ans