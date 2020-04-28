# 专栏分析

## 排序及其变形问题

### 快速排序

面试题40的最优解法：快速选择算法

### 归并排序（分治）

首先，需要熟练掌握归并排序的两种形式，一种是输入参数为数列的，另一种是直接对数组进行伪原地操作的，看一下第二种的写法：

```python
def merge(l:int,mid:int,r:int)->None:
    i,j,tmp = l,mid+1,[]
    while 1:
        while i<=mid and nums[i]<=nums[j]:
            tmp.append(nums[i])
            i+=1
        if i>mid:
            break
        while j<=r and nums[j]<nums[i]:
            tmp.append(nums[j])
            j+=1
        if j>r:
            break
    if j>r:
        tmp = tmp+nums[i:mid+1]
    if i>mid:
        tmp = tmp+nums[j:r+1]
    nums[l:r+1] = tmp
def mergesort(l:int,r:int)->None:
    if l>=r:
        return
    mid = (l+r)//2
    mergesort(l,mid)
    mergesort(mid+1,r)
    merge(l,mid,r)
mergesort(0,len(nums)-1)
print(nums)
```

经典的应用就是求逆序对个数，本质上是一种非常经典的分治思想。只需要对上述代码做简单的修改：将mergesort()函数和merge()函数的返回值改为int类型，表示返回本身中的逆序对和分处两边的逆序对。然后在l>=r的情况下直接返回0。在merge的过程中注意，每次加入右边（所以突然想到归并的稳定性真的是优越）的元素时，加和左边剩余元素个数（因为只有这样的一对构成逆序对），即可在O(nlogn)的时间复杂度下求解逆序对问题。



### 堆排序与优先队列

下面给出的是第23题合并k个有序列表的优先队列解法：

```python
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
```

这里要注意的是，q.put放进去的应当是一个元组，不然拿出来的时候会有问题。并且我测试python2和python3的优先队列在这里有区别，Python2好像是支持放不可哈希的关键字的（不参与排序）。但是python3似乎并不行。



## 搜索

### 回溯

经典题型莫过于解数独和N皇后了。

下面这一段是解数独的核心代码

```python
def judge(x:int,y:int,n:int)->bool:
    for i in range(9):
        if map[i][y] == n:
            return False
        if map[x][i] == n:
            return False
        xx, yy = 3*(x//3)+i//3, 3*(y//3)+i%3
        if map[xx][yy] == n:
            return False
    return True
def dfs(x:int,y:int)->True:
    exist = 0
    for k in range(9):
        if judge(x,y,k+1):
            map[x][y] = k+1
            flag = 0
            exist = 1
            for i in range(9):
                if flag:
                    break
                for j in range(9):
                    if not map[i][j]:
                        flag = 1
                        xn, yn = i,j
                        break
            if not flag:
                return True
            if dfs(xn,yn):
                return True
            map[x][y] = 0
    if not exist:
        return False
```

【数独】关键点有几处：一是judge函数判断方案是否可行，不需要判断整个棋盘，只需要判断新增的这一处影响到的区域就行。二是回溯的擦除，在dfs中调用dfs()后要逆序依次将之前填上的map位置擦掉，这相当于一个弹栈的过程。三是双层循环break要注意设flag变量，因为break只能退出一层；尽管这在本题中无关紧要，但是在别的地方可能非常致命。

下面是N皇后的代码

```python
def judge(x:int,y:int)->bool:
    for i in range(n):
        if map[i][y]:
            return False
    for xx in range(max(0,x+y-n+1),min(x+y+1,n)):
        yy = x+y-xx
        if map[xx][yy]:
            return False
    for xx in range(max(0,x-y),min(x-y+n,n)):
        yy = xx-x+y
        if map[xx][yy]:
            return False
    return True
def dfs(r:int)->None:
    for c in range(n):
        if judge(r,c):
            map[r][c] = 1
            if r==n-1:
                ans.append(trans(map))
                map[r][c] = 0
                return
            dfs(r+1)
            map[r][c] = 0
dfs(0)
```

【N皇后】这个跟数独很像，经典的回溯题。需要注意的问题是：①判断对角线的时候注意取值范围；②对地图的擦除，因为N皇后是找到所有的解，所以最后一步的赋值擦除也是要做的（不然第N行总是会有个东西占着，不会影响同行，会影响对角线的判断和最终结果）。最后一步的擦除不在回溯之中，而是在你记录并返回之前，要把最后一步填上的皇后删掉。【注意】也可以写在回溯之中，在dfs(r+1)前添加条件，就是没有找完的情况下再找下一步，这样写应该更加正统一点③对全结果的记录，要特别注意数组的深拷贝和浅拷贝问题，以及数值和列表在函数内外传递的区别（传值？传址？）



### 广搜





## 动态规划

### 背包

面试题

### 区间动规

### 树状动规



## 树

### 二叉树

### 字典树



## 图



## 其他小技巧

### 双指针

快慢指针：

经典的翻转链表：

```java
public ListNode reverseList(ListNode head) {
	ListNode pre = null;
	ListNode cur = head;
	ListNode tmp = null;
	while(cur!=null) {
		tmp = cur.next;
		cur.next = pre;
		pre = cur;
		cur = tmp;
	}
	return pre;
}
```

### 快速幂

下面附上的是极为经典的矩阵快速幂求斐波那契数列的代码

```python
class Solution:
    def fib(self, n: int) -> int:
        def multi(x:List[List[int]], y:List[List[int]]) -> List[List[int]]:
            m = len(x)
            n = len(x[0])
            s = len(y[0])
            tmp = [[0 for i in range(s)]for j in range(m)]
            for i in range(m):
                for j in range(n):
                    for k in range(s):
                        tmp[i][k] += x[i][j]*y[j][k] % 1000000007
            return tmp
        fib = [[0,1],[1,1]]
        a = [[0],[1]]
        while n>0:
            if n & 1 == 1:
                a = multi(fib,a)
            n = n//2
            fib = multi(fib,fib)
        return a[0][0] % 1000000007
```

### 位运算(+python reduce)

```python
from functools import reduce
class Solution:
    def singleNumbers(self, nums: List[int]) -> List[int]:
        xor, dif, ans1, ans2 = reduce(lambda x,y:x^y,nums), 1 ,0, 0
        while not dif & xor:
            dif <<= 1
        for i in nums:
            if i & dif:
                ans1 ^= i
            else:
                ans2 ^= i
        return [ans1,ans2]
```

【求落单元素】经典位运算，首先，如果要找出双元素数组中唯一落单的那个，可以直接异或。如果有两个落单的，可以异或得到两个数的异或值，然后找到出现不同的位置，用与运算将原数组分为两类，一类中包含一个落单的，并且相同的数字一定在同一类中。对两类分别累计异或即可得到想要的两个值。

【注意】学习reduce的用法