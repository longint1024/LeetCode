class Solution:
    def divingBoard(self, shorter: int, longer: int, k: int) -> List[int]:
        ans = [0]
        for i in range(k+1):
            j = k-i
            tmp = j*shorter + i*longer
            if tmp>ans[-1]:
                ans.append(tmp)
        return ans[1::]