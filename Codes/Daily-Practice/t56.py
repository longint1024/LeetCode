class Solution:
    def merge(self, intervals: List[List[int]]) -> List[List[int]]:
        if intervals == []:
            return []
        intervals.sort()
        index, n = 0, len(intervals)
        ans = [intervals[0]]
        for i in range(1,n):
            if ans[len(ans)-1][1] >= intervals[i][0]:
                ans[len(ans)-1] = [ans[len(ans)-1][0],max(intervals[i][1],ans[len(ans)-1][1])]
            else:
                ans.append(intervals[i])
        return ans