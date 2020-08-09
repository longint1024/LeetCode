# Definition for a binary tree node.
# class TreeNode:
#     def __init__(self, val=0, left=None, right=None):
#         self.val = val
#         self.left = left
#         self.right = right
class Solution:
    def recoverTree(self, root: TreeNode) -> None:
        ans = []
        def mids(root:TreeNode) -> None:
            if root.left:
                mids(root.left)
            ans.append(root.val)
            if root.right:
                mids(root.right)
        mids(root)
        r1, r2, n = -1, -1, len(ans)
        for i in range(n-1):
            if ans[i]>ans[i+1]:
                if r1==-1:
                    r1 = i
                r2 = i+1
        r1, r2 = ans[r1], ans[r2]
        #print(ans)
        #print([r1,r2])
        def change(root:TreeNode,r1:int,r2:int) -> None:
            if not root:
                return
            if root.val == r1:
                root.val = r2
            elif root.val == r2:
                root.val = r1
            change(root.left,r1,r2)
            change(root.right,r1,r2)
        change(root,r1,r2)
        return root