# Definition for a binary tree node.
# class TreeNode:
#     def __init__(self, x):
#         self.val = x
#         self.left = None
#         self.right = None

class Solution:
    def averageOfLevels(self, root: TreeNode) -> List[float]:
        ans, bfs = [], [root]
        while bfs:
            tmp, cnt, tot = [], 0.0, len(bfs)
            for node in bfs:
                cnt += node.val
                if node.left:
                    tmp.append(node.left)
                if node.right:
                    tmp.append(node.right)
            bfs = tmp
            ans.append(cnt/tot)
        return ans