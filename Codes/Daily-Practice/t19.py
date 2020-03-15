# Definition for singly-linked list.
# class ListNode:
#     def __init__(self, x):
#         self.val = x
#         self.next = None

class Solution:
    def removeNthFromEnd(self, head: ListNode, n: int) -> ListNode:
        now = head
        num = 0
        while now.next!=None:
            num = num+1
            now = now.next
        index = num - n + 1
        if num == 0:
            if n == 1:
                return None
            return head
        num = 0
        now = head
        print(index)
        if(index==0):
            return head.next
        while 1:
            num = num+1
            if num == index:
                break
            now = now.next
        now.next = now.next.next
        return head
        