class Solution:
    def visitOrder(self, points: List[List[int]], direction: str) -> List[int]:
        n = len(points)
        ans = []
        v = [1]*n
        def judge(s:int,m:int,e:int,tot:int)->bool:
            l1x, l1y = points[m][0]-points[s][0],points[m][1]-points[s][1]
            l2x, l2y = points[e][0]-points[m][0],points[e][1]-points[m][1]
            d = l1x*l2y-l1y*l2x
            if d >0 and direction[tot]=='L':
                return True
            if d<0 and direction[tot]=='R':
                return True
            return False
            
        def dfs(s:int,m:int,e:int,tot:int)->bool:
            if tot == n:
                return True
            if tot==0:
                for i in range(n):
                    v[i] = 0
                    if dfs(n,n,i,1):
                        ans.append(i)
                        return True
                    v[i] = 1
            if tot == 1:
                for i in range(n):
                    if v[i]:
                        v[i] = 0
                        if dfs(n,e,i,2):
                            ans.append(i)
                            return True
                        v[i] = 1
            if tot >= 2:
                flag = 0
                for i in range(n):
                    if v[i] and judge(m,e,i,tot-2):
                        flag = 1
                        v[i] = 0
                        if dfs(m,e,i,tot+1):
                            ans.append(i)
                            return True
                        v[i] = 1
                if not flag:
                    return False   
                    
        if dfs(n,n,n,0):
            ans.reverse()
            return ans