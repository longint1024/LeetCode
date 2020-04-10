class Solution:
    def generateParenthesis(self, n: int) -> List[str]:
        front, tail = -1, 0
        queue = ['']
        ans = []
        while front<tail:
            front += 1
            s = queue[front]
            if len(s)==2*n:
                ans.append(s)
                continue
            l, r = s.count('('), s.count(')')
            if l<n:
                queue.append(s+'(')
                tail+=1
            if r<l:
                queue.append(s+')')
                tail+=1
        return ans