class Solution:
    def intersection(self, nums1: List[int], nums2: List[int]) -> List[int]:
        ans,a,b = [],set(nums1),set(nums2)
        if len(a)<len(b):
            for i in a:
                if i in b:
                    ans.append(i)
        else:
            for i in b:
                if i in a:
                    ans.append(i)
        return ans