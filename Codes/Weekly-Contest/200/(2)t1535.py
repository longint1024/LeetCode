class Solution:
    def getWinner(self, arr: List[int], k: int) -> int:
        n = len(arr)
        p = k
        if k>2*n+1:
            p = 2*n+1
        time = 0
        while 1:
            flag = 1
            if time:
                k = p-1
            else:
                k = p
            for i in range(k):
                #print(arr)
                if arr[0]>arr[1]:
                    tmp = arr[1]
                    arr.remove(tmp)
                    arr.append(tmp)
                else:
                    tmp = arr[0]
                    arr.remove(tmp)
                    arr.append(tmp)
                    flag = 0
                    time = 1
                    break
            if flag:
                return arr[0]