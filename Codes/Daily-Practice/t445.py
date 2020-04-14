# Definition for singly-linked list.
# class ListNode:
#     def __init__(self, x):
#         self.val = x
#         self.next = None

class Solution:
    def addTwoNumbers(self, l1: ListNode, l2: ListNode) -> ListNode:
        if not l1 and not l2:
            return None
        now, num1 = l1, 0
        while now:
            num1 = num1 * 10 + now.val
            now = now.next
        now, num2 = l2, 0
        while now:
            num2 = num2 * 10 + now.val
            now = now.next
        num = num1+num2
        ans = None
        if num == 0:
            return ListNode(0)
        while num>0:
            now = ListNode(num%10)
            now.next = ans
            ans = now
            num = num // 10
        return ans