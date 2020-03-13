# Definition for singly-linked list.
# class ListNode:
#     def __init__(self, x):
#         self.val = x
#         self.next = None

class Solution:
    def mergeKLists(self, lists: List[ListNode]) -> ListNode:
        if lists == []:
            return []
        def merge2(l1:ListNode,l2:ListNode)->ListNode:
            if l1 == None:
                return l2
            if l2 == None:
                return l1
            if l1.val<l2.val:
                ans = ListNode(l1.val)
                l1 = l1.next
            else:
                ans = ListNode(l2.val)
                l2 = l2.next
            now = ans
            while 1:
                if l1 == None:
                    now.next = l2
                    return ans
                if l2 == None:
                    now.next = l1
                    return ans
                if l1.val<l2.val:
                    new = ListNode(l1.val)
                    now.next = new
                    now = now.next
                    l1 = l1.next
                else:
                    new = ListNode(l2.val)
                    now.next = new
                    now = now.next
                    l2 = l2.next
        def merge(left:int, right:int)->ListNode:
            if left == right:
                return lists[left]
            mid = (left+right)//2
            return merge2(merge(left,mid),merge(mid+1,right))
        return merge(0,len(lists)-1)