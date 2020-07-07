# Definition for a binary tree node.
# class TreeNode:
#     def __init__(self, x):
#         self.val = x
#         self.left = None
#         self.right = None

class Solution:
    def hasPathSum(self, root: TreeNode, sum: int) -> bool:
        if not root:
            return False
        s = [root]
        while 1:
            tmp = []
            for i in s:
                flag = 0
                if i.left:
                    i.left.val += i.val
                    tmp.append(i.left)
                    flag = 1
                if i.right:
                    i.right.val += i.val
                    tmp.append(i.right)
                    flag = 1
                if not flag:
                    if i.val == sum:
                        return True
            if tmp == []:
                break
            s = tmp
        return False