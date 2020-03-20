# Definition for singly-linked list.
# class ListNode:
#     def __init__(self, x):
#         self.val = x
#         self.next = None

class Solution:
    def swapPairs(self, head: ListNode) -> ListNode:
        thead = ListNode(0)
        thead.next = head
        now = thead
        while 1:
            if now.next == None or now.next.next == None:
                break
            tmp = now.next
            now.next = tmp.next
            tmp.next = now.next.next
            now.next.next = tmp
            now = now.next.next
        return thead.next