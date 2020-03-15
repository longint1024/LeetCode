# Definition for a binary tree node.
# class TreeNode:
#     def __init__(self, x):
#         self.val = x
#         self.left = None
#         self.right = None

class Solution:
    def balanceBST(self, root: TreeNode) -> TreeNode:
        arr = []
        def todo(node: TreeNode) ->None:
            arr.append(node.val)
            if node.left == None and node.right == None:
                return 0
            if node.left != None:
                todo(node.left)
            if node.right != None:
                todo(node.right)
        todo(root)
        arr.sort()
        n = len(arr)
        ans = TreeNode(0)
        def creat(l: int, r: int) -> TreeNode:
            if l == r:
                new = TreeNode(arr[l])
                node = new
                return new
            if l>r:
                return None
            mid = (l+r)//2
            new = TreeNode(arr[mid])
            new.left = creat(l,mid-1)
            new.right = creat(mid+1,r)
            return new
        ans = creat(0,n-1)
        return ans