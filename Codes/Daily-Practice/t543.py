# Definition for a binary tree node.
# class TreeNode:
#     def __init__(self, x):
#         self.val = x
#         self.left = None
#         self.right = None

class Solution:
    def diameterOfBinaryTree(self, root: TreeNode) -> int:
        self.MAX = 0
        if root == None:
            return 0
        if root.left == None and root.right == None:
            return 0
        def path(node: TreeNode) -> int:
            if node.left == None and node.right == None:
                return 0
            if node.left == None:
                lef = 0
            else:
                lef = 1+path(node.left)
            if node.right == None:
                rig = 0
            else:
                rig = 1+path(node.right)
            if lef+rig>self.MAX:
                self.MAX = lef+rig
            return max(lef,rig)
        tmp = path(root)
        return self.MAX