# Definition for a binary tree node.
# class TreeNode:
#     def __init__(self, val=0, left=None, right=None):
#         self.val = val
#         self.left = left
#         self.right = right
class Solution:
    def generateTrees(self, n: int) -> List[TreeNode]:
        def gt(l:int,r:int)->List[List[TreeNode]]:
            if l>r:
                return [None]
            alltrees = []
            for i in range(l,r+1):
                lefttrees = gt(l,i-1)
                righttrees = gt(i+1,r)
                for lt in lefttrees:
                    for rt in righttrees:
                        tmp = TreeNode(i)
                        tmp.left = lt
                        tmp.right = rt
                        alltrees.append(tmp)
            return alltrees
        return gt(1,n) if n else []