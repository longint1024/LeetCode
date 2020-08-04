class Solution:
    def maxSum(self, nums1: List[int], nums2: List[int]) -> int:
        i1,i2 = 1,1
        n1,n2 = len(nums1),len(nums2)
        index1,index2 = [-1 for i in range(n1)],[-1 for i in range(n2)]
        c1,c2 = 0,0
        M = 10**9+7
        for i in range(n1):
            if c2>n2-1:
                break
            while nums1[i] > nums2[c2]:
                c2 += 1
                if c2>n2-1:
                    break
            if c2>n2-1:
                break
            if nums1[i] == nums2[c2]:
                index1[i] = c2
                c2 += 1
                continue
        for i in range(n2):
            if c1>n1-1:
                break
            while nums2[i] > nums1[c1]:
                c1 += 1
                if c1>n1-1:
                    break
            if c1>n1-1:
                break
            if nums2[i] == nums1[c1]:
                index2[i] = c1
                c1 += 1
                continue
                
                
        d1,d2 = [0 for i in range(n1+1)], [0 for i in range(n2+1)]
        while 1:
            if i1>n1 or  i2>n2:
                break
            if nums1[i1-1]<=nums2[i2-1]:
                d1[i1] = max(d1[i1],d1[i1-1]+nums1[i1-1])
                if index1[i1-1] == -1:
                    pass
                else:
                    d1[i1] = max(d1[i1],d2[index1[i1-1]])  
                    d2[index1[i1-1]+1] = d1[i1]
                i1+=1
            if i1>n1 or  i2>n2:
                break
            if nums2[i2-1]<=nums1[i1-1]:
                d2[i2] = max(d2[i2],d2[i2-1]+nums2[i2-1])
                if index2[i2-1] == -1:
                    pass
                else:
                    d2[i2] = max(d2[i2],d1[index2[i2-1]])  
                    d1[index2[i2-1]+1] = d2[i2]
                i2+=1
        while i1<=n1:
            d1[i1] = max(d1[i1],d1[i1-1]+nums1[i1-1])
            if index1[i1-1] == -1:
                pass
            else:
                d1[i1] = max(d1[i1],d2[index1[i1-1]])  
                d2[index1[i1-1]+1] = d1[i1]
            i1+=1
        while i2<=n2:
            d2[i2] = max(d2[i2],d2[i2-1]+nums2[i2-1])
            if index2[i2-1] == -1:
                pass
            else:
                d2[i2] = max(d2[i2],d1[index2[i2-1]])  
                d1[index2[i2-1]+1] = d2[i2]
            i2+=1
        return max(d1[n1],d2[n2])%M
                