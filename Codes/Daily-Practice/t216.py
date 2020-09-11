class Solution:
    def combinationSum3(self, k: int, n: int) -> List[List[int]]:
        ans = []
        def com(k:int,index:int,n:int,c:List[int]):
            if index>9:
                return
            if n<index:
                return
            if k == 1  and n<=9:
                tmp = [_ for _ in c]
                tmp.append(n)
                ans.append(tmp)
            if k*9<n:
                return
            if k*index>n:
                return
            if k+index>10:
                return
            for i in range(index,10):
                com(k-1,i+1,n-i,c+[i])
        com(k,1,n,[])
        return ans