# Definition for a binary tree node.
# class TreeNode:
#     def __init__(self, x):
#         self.val = x
#         self.left = None
#         self.right = None

class Solution:
    def sortedArrayToBST(self, nums: List[int]) -> TreeNode:
        n = len(nums)
        if not n:
            return None
        def buildTree(left:int,right:int)->TreeNode:
            if left>right:
                return None
            mid = (left+right+1)//2
            root = TreeNode(nums[mid])
            root.left = buildTree(left,mid-1)
            root.right = buildTree(mid+1,right)
            return root
        return buildTree(0,n-1)