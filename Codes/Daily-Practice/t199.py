# Definition for a binary tree node.
# class TreeNode:
#     def __init__(self, x):
#         self.val = x
#         self.left = None
#         self.right = None

class Solution:
    def rightSideView(self, root: TreeNode) -> List[int]:
        if root == None:
            return []
        node = [root]
        ans = []
        while 1:
            ans.append(node[len(node)-1].val)
            tmp = []
            for i in node:
                if i.left:
                    tmp.append(i.left)
                if i.right:
                    tmp.append(i.right)
            if tmp == []:
                return ans
            node = tmp