# Definition for a binary tree node.
# class TreeNode:
#     def __init__(self, x):
#         self.val = x
#         self.left = None
#         self.right = None

class Solution:
    def levelOrder(self, root: TreeNode) -> List[List[int]]:
        if not root:
            return []
        tree = [[root]]
        ans = [[root.val]]
        while 1:
            tmp = []
            add = []
            for i in tree[len(ans)-1]:
                if i.left:
                    tmp.append(i.left)
                    add.append(i.left.val)
                if i.right:
                    tmp.append(i.right)
                    add.append(i.right.val)
            if tmp == []:
                break
            tree.append(tmp)
            ans.append(add)
        return ans