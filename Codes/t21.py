# Definition for singly-linked list.
# class ListNode:
#     def __init__(self, x):
#         self.val = x
#         self.next = None

class Solution:
    def mergeTwoLists(self, l1: ListNode, l2: ListNode) -> ListNode:
        head = ListNode(-1)
        ans = ListNode(-1)
        head.next = ans
        while 1:
            if l1==None:
                ans.next = l2
                break
            if l2==None:
                ans.next = l1
                break
            if (l1.val<=l2.val):
                now = ListNode(l1.val)
                l1 = l1.next
                ans.next = now
                ans = ans.next
            else:
                now = ListNode(l2.val)
                l2 = l2.next
                ans.next = now
                ans = ans.next
        return head.next.next