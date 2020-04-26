from queue import PriorityQueue
class Solution:
    def constrainedSubsetSum(self, nums: List[int], k: int) -> int:
        n = len(nums)
        ans = nums
        pq = PriorityQueue()
        pq.put(-ans[0])
        index = -1
        MAX = 0
        for i in range(1,n):
            if index==max(0,i-k)-1:
                MAX = 0
                for j in range(max(0,i-k),i):
                    if ans[j]>MAX:
                        MAX = ans[j]
                        index = j      
            print(index,MAX)
            if MAX>0:
                ans[i] += MAX
            if ans[i]>MAX:
                MAX = ans[i]
                index = i
        print(ans)
        MAX = -1000000000
        for i in ans:
            if i>MAX:
                MAX = i
        return MAX