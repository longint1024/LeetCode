# Definition for a binary tree node.
# class TreeNode:
#     def __init__(self, x):
#         self.val = x
#         self.left = None
#         self.right = None

class Solution:
    def maxDepth(self, root: TreeNode) -> int:
        self.max = -1
        def deep(node: TreeNode,d):
            if node == None:
                if d>self.max:
                    self.max = d
                return
            deep(node.left,d+1)
            deep(node.right,d+1)
        deep(root,0)
        return self.max