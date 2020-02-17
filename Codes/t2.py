# Definition for singly-linked list.
# class ListNode:
#     def __init__(self, x):
#         self.val = x
#         self.next = None

class Solution:
    def addTwoNumbers(self, l1: ListNode, l2: ListNode) -> ListNode:
        dummy=ListNode(-1)
        ans=dummy
        carry = 0
        while l1 or l2:
            num1, num2 = l1.val if l1 else 0, l2.val if l2 else 0
            num =  num1 + num2 +carry
            carry = 0
            if(num>9):
                num = num-10
                carry = 1
            ans.next = ListNode(num)
            l1, l2 = l1.next if l1 else None, l2.next if l2 else None
            ans = ans.next
        if (carry):
            ans.next = ListNode(carry)
        return dummy.next