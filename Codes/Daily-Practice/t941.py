class Solution:
    def validMountainArray(self, A: List[int]) -> bool:
        up, n = 1, len(A)
        if n<3:
            return False
        if A[1]<A[0]:
            return False
        while up<n and A[up]>A[up-1]:
            up += 1
        if up == n:
            return False
        while up<n and A[up]<A[up-1]:
            up += 1
        return up==n