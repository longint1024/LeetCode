# Definition for singly-linked list.
# class ListNode:
#     def __init__(self, x):
#         self.val = x
#         self.next = None

from queue import PriorityQueue

class Solution:
    def mergeKLists(self, lists: List[ListNode]) -> ListNode:
        if lists == []:
            return []
        head = point = ListNode(0)
        q = PriorityQueue()
        for k in range(len(lists)):
            if lists[k]:
                q.put((lists[k].val, k))
        while not q.empty():
            val, num = q.get()
            point.next = ListNode(val)
            point = point.next
            hh = lists[num]
            tmp = hh.next
            lists[num] = tmp
            if lists[num]:
                q.put((lists[num].val, num))
        return head.next