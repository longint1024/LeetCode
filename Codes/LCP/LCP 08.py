class Solution:
    def getTriggerTime(self, increase: List[List[int]], requirements: List[List[int]]) -> List[int]:
        crh = [0,0,0]
        ans = [-1 for i in range(len(requirements))]
        for i in range(len(requirements)):
            requirements[i].append(i)
        requirements.sort()
        print(requirements)
        index = 0
        for k in range(len(requirements)):
                if crh[0]>=requirements[k][0] and crh[1]>=requirements[k][1] and crh[2]>=requirements[k][2]:
                    if ans[requirements[k][3]]==-1:
                        ans[requirements[k][3]] = 0
        MIN = 0
        for i in range(len(increase)):
            for j in range(3):
                crh[j] += increase[i][j]
            print(crh,index)
            flag = 0
            MIN = index
            for k in range(index,len(requirements)):
                if crh[0]>=requirements[k][0] and crh[1]>=requirements[k][1] and crh[2]>=requirements[k][2]:
                    if ans[requirements[k][3]] == -1:
                        ans[requirements[k][3]] = i+1
                else:
                    if not flag:
                        MIN = k
                        flag = 1
                if crh[0]<requirements[k][0]:
                    index = min(k,MIN)
                    break
        return ans