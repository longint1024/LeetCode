class Solution:
    def canFinish(self, numCourses: int, prerequisites: List[List[int]]) -> bool:
        inset = [0 for i in range(numCourses)]
        point = [[]for i in range(numCourses)]
        nset = [i for i in range(numCourses)]
        for e in prerequisites:
            inset[e[0]] += 1
            point[e[1]].append(e[0])
        count = 0
        while 1:
            tmp = []
            for i in nset:
                if not inset[i]:
                    tmp.append(i)
            n0 = len(tmp)
            count += n0
            if count == numCourses:
                return True
            if not n0:
                return False
            for i in tmp:
                for k in point[i]:
                    inset[k] -= 1
            for i in tmp:    
                nset.remove(i)