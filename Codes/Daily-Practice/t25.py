# Definition for singly-linked list.
# class ListNode:
#     def __init__(self, x):
#         self.val = x
#         self.next = None

class Solution:
    def reverseKGroup(self, head: ListNode, k: int) -> ListNode:
        thead = ListNode(0)
        thead.next = head
        now = thead
        while 1:
            tmp1 = now
            tmp2 = now.next
            flag = 1
            for i in range(k):
                if now.next == None:
                    flag = 0
                    break
                now = now.next
            if not flag:
                break
            tmp3 = now.next
            tmp1.next = now
            num = k-2
            while num>=0:
                node = tmp2
                for i in range(num):
                    node = node.next
                now.next = node
                now = node
                num -= 1
            tmp2.next = tmp3
            now = tmp2
        return thead.next