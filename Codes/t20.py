class Solution:
    def isValid(self, s: str) -> bool:
        stack = []
        num = -1
        lens =  len(s)
        left = ["(","[","{"]
        right = [")","]","}"]
        flag = 1
        for i in range(lens):
            if s[i] in left:
                for j in range(3):
                    if s[i] == left[j]:
                        num = num+1
                        stack.append(j)
            if s[i] in right:
                if (num==-1):
                    flag = 0
                    break
                for j in range(3):
                    if s[i] == right[j]:
                        flag = 0
                        if stack[num] == j:
                            flag = 1
                        if flag:
                            del stack[num]
                            num = num -1
                        break
            if not flag:
                break
        if num != -1:
            return 0
        return flag