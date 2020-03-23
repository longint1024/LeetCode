# Definition for singly-linked list.
# class ListNode:
#     def __init__(self, x):
#         self.val = x
#         self.next = None

class Solution:
    def middleNode(self, head: ListNode) -> ListNode:
        now = head
        num = 0
        while now:
            num += 1
            now = now.next
        now = head
        for i in range(num//2):
            now = now.next
        return now