# 专栏分析

## 基本数据结构

### 链表

下面是一个合并有序链表的程序，还是有需要注意的东西的

```python
class Solution:
    def mergeTwoLists(self, l1: ListNode, l2: ListNode) -> ListNode:
        head = ListNode(0)
        now = head
        while 1:
            if not l2:
                now.next = l1
                break
            while l1 and l1.val<=l2.val:
                now.next = ListNode(l1.val)
                now, l1 = now.next, l1.next
            if not l1:
                now.next = l2
                break
            while l2 and l2.val<l1.val:
                now.next = ListNode(l2.val)
                now, l2 = now.next, l2.next
        return head.next
```

【注意】这里细节有两个，首先if not l2是必须的，因为l2有可能本身就是空的，所以要写在最前面。l1不停地向后的过程中，有可能变成None而退出第一个内层循环，这时要注意判断并退出，所以后面跟的if not l1也是必须的。

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

【注意】默认关键字是越小越好，最小的数字最先出队。

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

【N皇后】这个跟数独很像，经典的回溯题。需要注意的问题是：①判断对角线的时候注意取值范围；②对地图的擦除，因为N皇后是找到所有的解，所以最后一步的赋值擦除也是要做的（不然第N行总是会有个东西占着，不会影响同行，会影响对角线的判断和最终结果）。最后一步的擦除不在回溯之中，而是在你记录并返回之前，要把最后一步填上的皇后删掉。【注意】也可以写在回溯之中，在dfs(r+1)前添加条件，就是没有找完的情况下再找下一步，这样写应该更加正统一点③对全结果的记录，要特别注意数组的深拷贝和浅拷贝问题，以及数值和列表在函数内外传递的区别（传值与传址），当然了python有它函数式编程的说法，本质上看起来个人感觉还是面向内存的问题。

```python
class Solution:
    ans = 0
    def totalNQueens(self, n: int) -> int:
        map = [[1]*n for i in range(n)]
        self.ans = 0
        def sweep(r:int,c:int,e:int)->None:
            for i in range(n):
                map[i][c] -= e
            for i in range(max(0,r+c-n+1),min(r+c+1,n)):
                map[i][r+c-i] -= e
            for i in range(max(0,r-c),min(r-c+n,n)):
                map[i][i+c-r] -= e
        def dfs(r:int)->None:
            for c in range(n):
                if map[r][c]==1:
                    if r == n-1:
                        self.ans += 1
                        return
                    sweep(r,c,1)
                    dfs(r+1)
                    sweep(r,c,-1)
            return
        dfs(0)
        return self.ans
```

【N皇后】这次我试了另一种途径：用map来标记占用区域，这样可以避免重复判断。注意python外部变量在函数内部不能被改变（除非传的是地址），所以我觉得要把变量绑定到地址上，一试self指针果然可以。这题需要注意的地方是，sweep清除横竖斜行的占用时，不能直接把所有占用都清掉了，因为可能把不输入它的别的占用也给清掉了。所以我用map记录的实际上是“被占用次数”，清除就加回去一次。直到所有限制都被解禁才可以使用。

【思考】当然也可以这样：用map来记录可否使用，放置每个皇后时，考虑由这个皇后引入的“新增”的禁用区域，回溯时只释放“新增”的禁用区域即可。



### 广搜





## 动态规划

### 递推

我本来想把此类问题命名为“简单动态规划”，以分类在解决此类问题的过程中，经常出现一种简单的思路。比如上台阶这种递推，稍微复杂一点的比如：最长不下降子序列、最长重复子序列等等。

比如很经典的一个问题，寻找两个数组的最长重复子数组。同样是以空间换时间，将前缀最大长度做好记录。为了将递推的数组表示为子问题的形式，应当假定当前位必须被包含。

```python
class Solution:
    def findLength(self, A: List[int], B: List[int]) -> int:
        m, n, MAX = len(A), len(B), 0
        dp = [[0 for i in range(n+1)]for j in range(m+1)]
        for i in range(1,m+1):
            for j in range(1,n+1):
                if A[i-1]==B[j-1]:
                    dp[i][j] = dp[i-1][j-1]+1
                else:
                    dp[i][j] = 0
                if dp[i][j]>MAX:
                    MAX = dp[i][j]
        return MAX
```



### 背包

面试题

### 区间动规

### 树状动规



## 树

### 二叉树

#### Binary Search Tree

话不多说，上代码，中序遍历判断是否是BST

```python
class Solution:
    def isValidBST(self, root: TreeNode) -> bool:
        stack, inorder = [], float('-inf')
        print(inorder)
        while stack or root:
            while root:
                stack.append(root)
                root = root.left
            root = stack.pop()
            # 如果中序遍历得到的节点的值小于等于前一个 inorder，说明不是二叉搜索树
            if root.val <= inorder:
                return False
            inorder = root.val
            root = root.right

        return True
```



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

### 位运算(+python3 reduce)

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

【注意】学习reduce的用法，另外，python3中reduce放在functools里面，而不是像Python2那样作为内置函数