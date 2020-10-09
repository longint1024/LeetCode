# 专栏分析

## 基本数据结构

### 列表、元组与集合

```python
list.remove(a)    #：删掉首个值为a的元素，此操作在关于list的循环中谨慎使用

del list[j]    #：删掉index为j的列表元素，此操作在关于list的循环中谨慎使用

list.insert(i,a)    #：在index为i的位置增添a元素，其后元素依次后移一位
```

### 字符串

```python
str.upper()    #将字符串中所有字符转为大写
str.lower()    #将字符串中所有字符转为小写
```

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

### 栈

### 队列

#### 双向队列

经典的是双向队列解决滑动窗口最大值问题。滑动窗口连续和最大可以用前缀和解决，滑动窗口内最大值可以在线性时间复杂度内实现，实现方式有双向队列和动态规划。

```python
#t239 滑动窗口最大值-双向队列实现
from collections import deque
class Solution:
    def maxSlidingWindow(self, nums: List[int], k: int) -> List[int]:
        n = len(nums)
        if not (n and k):
            return []
        if k==1:
            return nums
        dq, ans = deque(), []
        def cleardq(i:int)->None:
            if dq and dq[0]==i-k:
                dq.popleft()
            while dq and nums[i]>nums[dq[-1]]:
                dq.pop()
        MAX = -1000000
        for i in range(k):
            cleardq(i)
            dq.append(i)
            if nums[i]>MAX:
                MAX = nums[i]
        ans.append(MAX)
        for i in range(k,len(nums)):
            cleardq(i)
            dq.append(i)
            ans.append(nums[dq[0]])
        return ans
```

### 指针、邻接表与拷贝（+哈希）

这一题就非常好的展示了内存访问、邻接表使用与深浅拷贝之间的关系。需要注意的是哈希表的用法，本题关于哈希表的写法是非常规范且简洁的

```python
#T133 克隆图
"""
# Definition for a Node.
class Node:
    def __init__(self, val = 0, neighbors = []):
        self.val = val
        self.neighbors = neighbors
"""

from collections import deque
class Solution(object):

    def cloneGraph(self, node):
        """
        :type node: Node
        :rtype: Node
        """

        if not node:
            return node

        visited = {}

        # 将题目给定的节点添加到队列
        queue = deque([node])
        # 克隆第一个节点并存储到哈希表中
        visited[node] = Node(node.val, [])

        # 广度优先搜索
        while queue:
            # 取出队列的头节点
            n = queue.popleft()
            # 遍历该节点的邻居
            for neighbor in n.neighbors:
                if neighbor not in visited:
                    # 如果没有被访问过，就克隆并存储在哈希表中
                    visited[neighbor] = Node(neighbor.val, [])
                    # 将邻居节点加入队列中
                    queue.append(neighbor)
                # 更新当前节点的邻居列表
                visited[n].neighbors.append(visited[neighbor])

        return visited[node]
```



## 排序及其变形问题

### 快速排序

面试题40的最优解法：快速选择算法

### 归并排序（分治）

首先，需要熟练掌握归并排序的两种形式，一种是输入参数为数列的，另一种是直接对数组进行伪原地操作的，看一下第二种的写法：

```python
#归并排序
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
#合并k个有序列表
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

【注意】默认关键字是**越小**越好，最小的数字最先出队。

这里要注意的是，q.put放进去的应当是一个元组，不然拿出来的时候会有问题。并且我测试python2和python3的优先队列在这里有区别，Python2好像是支持放不可哈希的关键字的（不参与排序）。但是python3似乎并不行。这可能和排序关键字的指定有关，我没有仔细研究。



## 搜索

### 回溯

经典题型莫过于解数独和N皇后了。

下面这一段是解数独的核心代码

```python
#解数独
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
#N皇后
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
#N皇后传递MAP
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

【24点】这道题状态的擦除值得注意，另外，对除零情况的考虑和跳过也非常有意思。本题的难点在于如何处理括号。自己写的代码可读性很差，官方代码对常变量的定义以及计算顺序的处理都很值得借鉴。

```python
#T679 24点游戏
class Solution:
    def judgePoint24(self, nums: List[int]) -> bool:
        def compute(num:List[int])-> bool:
            n = len(num)
            if n == 1:
                return abs(num[0]-24)<0.000001
            for i in range(n-1):
                for j in range(i+1,n):
                    new = []
                    for k in range(n):
                        if k!=i and k!=j:
                            new.append(num[k])
                    a, b = num[i], num[j]
                    for t in range(6):
                        if t == 0:
                            new.append(a+b)
                            if compute(new):
                                return True
                        elif t == 1:
                            new.append(a*b)
                            if compute(new):
                                return True
                        elif t == 2:
                            if b == 0:
                                continue
                            new.append(a/b)
                            if compute(new):
                                return True
                        elif t == 3:
                            if a == 0:
                                continue
                            new.append(b/a)
                            if compute(new):
                                return True
                        elif t == 4:
                            new.append(a-b)
                            if compute(new):
                                return True
                        elif t == 5:
                            new.append(b-a)
                            if compute(new):
                                return True
                        new.pop()
            return False
        return compute(nums)
```



### 广搜

#### 双向BFS



## 动态规划

### 递推

我本来想把此类问题命名为“简单动态规划”，以分类在解决此类问题的过程中，经常出现一种简单的思路。比如上台阶这种递推，稍微复杂一点的比如：最长不下降子序列、最长重复子序列等等。

比如很经典的一个问题，寻找两个数组的最长重复子数组。同样是以空间换时间，将前缀最大长度做好记录。为了将递推的数组表示为子问题的形式，应当假定当前位必须被包含。

```python
#最长重复子串
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

比如简单的迷宫走法总数问题，只能向右或向下：

```python
#障碍迷宫（+滚动数组->一维递推）
class Solution:
    def uniquePathsWithObstacles(self, obstacleGrid: List[List[int]]) -> int:
        m, n = len(obstacleGrid), len(obstacleGrid[0])
        if obstacleGrid[0][0]:
            return 0
        ans = [0 for i in range(n)]
        ans[0] = 1
        for i in range(m):
            for j in range(n):
                if obstacleGrid[i][j]:
                    ans[j] = 0
                else:
                    if j>0:
                        ans[j] += ans[j-1]
        return ans[n-1]
```

又有此类问题的延伸：如果要求路径和的最小值最大（走过路径求和，优化沿途的最小值），此类问题就不能直接套用上面这种动规方式。因为如果正向递推，会不满足无后效性原则。

#### 滚动数组

滚动数组是一种很重要的优化手段，值得单独拿出来总结一下。

比如T97：交错字符串。该题优化手段不像二维矩阵递推的滚动数组那样明显。

```python
#交错字符串，二维状态递推
class Solution:
    def isInterleave(self, s1: str, s2: str, s3: str) -> bool:
        n1, n2, n3 = len(s1), len(s2), len(s3)
        if n3 != n1+n2:
            return False
        dp = [[0 for i in range(n2+1)]for j in range(n1+1)]
        dp[0][0] = 1
        for i in range(n1+1):
            for j in range(n2+1):
                k = i+j
                if i>0 and dp[i-1][j] and s1[i-1] == s3[k-1]:
                    dp[i][j] = 1
                    continue
                if j>0 and dp[i][j-1] and s2[j-1] == s3[k-1]:
                    dp[i][j] = 1
        return bool(dp[n1][n2])
```

如果只使用一维递推，就不能直接在满足条件时赋值为真，因为dp[0]包含了多重含义，任何i对应的dp[i,0]都在dp[0]中。在二维数组中，每个dp[i,0]原本都占了个位置，本来就是零，所以可以在满足条件的情况下再改。但是一维数组不同，如果dp[i,0]不满足条件，它需要从0改成1。所以不能写成上面那样，不然就会出现伪判正。

```python
#交错字符串，一维状态递推
class Solution:
    def isInterleave(self, s1: str, s2: str, s3: str) -> bool:
        if len(s1)<len(s2):
            s1, s2 = s2, s1
        n1, n2, n3 = len(s1), len(s2), len(s3)
        if n3 != n1+n2:
            return False
        dp = [0 for i in range(n2+1)]
        dp[0] = 1
        for i in range(n1+1):
            for j in range(n2+1):
                k = i+j
                if i>0:
                    dp[j] = dp[j] and s1[i-1] == s3[k-1]
                if j>0:
                    dp[j] = dp[j] or (dp[j-1] and s2[j-1] == s3[k-1])
        return bool(dp[n2])
```

这是在改成滚动数组时很容易犯的错误，究其原因，是二维本身“有恃无恐”，它只需要判断是否应该从0改1。而一维数组的情况复杂些，初始状态的赋值可能仅仅对第一次迭代有效，对后面的迭代则情况不同。因此，如果直接二维改一维，需要做以下判断：①能否直接改？会不会影响之后的状态？②考虑到初始条件，公式是否有细微变化？如果有，改动，如果不好改，干脆将初始状态进入迭代态的那一步单独提出来做了，再进入迭代滚动。



### 记忆化搜索

#### 动态规划类

这类题目和第一类简单递推的思路其实差不多，问题在于它们常常看起来更像回溯。正向思路往往很难求解，构建逆向模型来描述问题看起来很有些像奇技淫巧。

比如T312戳气球，这题定义开区间、建立子问题的手段都是值得学习的。定义dp[i,j]表示开区间i到j戳气球能得到的最高分数，如果思考先戳哪个、再戳哪个，很容易陷入回溯搜索的思路。问题在于，对于这道题，回溯为什么复杂度超高？因为它重复计算了很多次：在回溯dp[i,k]、dp[k,j]的过程中，对每一个枚举的k向下继续分解，dp[i,k]、dp[k,j]都会被其它的k重复计算很多次，从而形成一个阶乘的复杂度。如果我们定义这样的数组来储存此结果，就可以大大减少计算量。但记忆化搜索还有另一个问题：如何确保在用dp[k,j]之前，它已经被计算并保存了呢？如果考虑清楚这个顺序，实际上它已经变成动态规划递推了。

有以上定义，显然当i>=j-1时，dp[i,j] = 0，这与初始化相同，不需要改变。由于k∈(i,j)，所以对dp[i,j]来说它需要的是这样一个倒三角形状的值。因此，i可以从n+1取到0倒着取，j从i+2正向取到n+1即可

|  ??  |  ??  |  ??  | ans  |
| :--: | :--: | :--: | :--: |
|      |  ??  |  ??  |  ??  |
|      |      |  ??  |  ??  |
|      |      |      |  ??  |

```python
#T312 戳气球
class Solution:
    def maxCoins(self, nums: List[int]) -> int:
        n = len(nums)
        nums.insert(0,1)
        nums.append(1)
        dp = [[0 for i in range(n+2)]for j in range(n+2)]
        for i in range(n+1,-1,-1):
            for j in range(i+2,n+2):
                for k in range(i+1,j):
                    if dp[i][k]+dp[k][j]+nums[i]*nums[j]*nums[k]>dp[i][j]:
                        dp[i][j] = dp[i][k]+dp[k][j]+nums[i]*nums[j]*nums[k]
        return dp[0][n+1]
```



#### 递推类

典型的如T1553，本题的数学公式解释写在周赛总结中了，关键在于，即使按照正确简洁的递归公式去做，也很难在规定时间内计算出正确结果。因此，加哈希的记忆化搜索是必不可少的。

```python
#T1553 吃掉N个橘子的最少天数
class Solution:
    def minDays(self, n: int) -> int:
        compute = {}
        def mind(n:int) -> int:
            if n in compute:
                return compute[n]
            if n == 1:
                return 1
            if n == 2 or n == 3:
                return 2
            c2 = mind(n//2)+ (n&1)
            c3 = mind(n//3) + n%3
            tmp = 1+min(c2,c3)
            compute[n] = tmp
            return tmp
        return mind(n)
```



### 背包

面试题

### 区间动规

周赛题T1547切棍子的最小成本与上面的记忆化搜索里的戳气球是典型的区间动规。

经典例题如LeetCode的T546——移除盒子。

### 树状动规



## 树

### 二叉树

#### Binary Search Tree

话不多说，上代码，中序遍历判断是否是BST

```python
#中序遍历判定BST
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



### 字典树（Trie）

LeetCode上有经典的**面试题17.13**，是字典树（Trie[Trai]读音参考特里亚，感觉很像“踹”）+动规的题目，当然可以用AC自动机。这道题的动规并不困难，棘手的地方是转移方程中有字符串与字典的匹配，这个一旦处理不好就会非常慢。

我测试了一下，如果不将字典转为集合，而是直接用列表判断是否存在，那么耗时会非常可怕（9112ms，顺带吐槽：这也能过？合着不哈希也不卡时间的？），查询复杂度应该在O(m)。将字典转换为set()后查询，由于哈希的存在，复杂度较低，但常数很大（860ms）。下面给出用哈希的代码：

```python
#Hash-Table 单词最优匹配
class Solution:
    def respace(self, dictionary: List[str], sentence: str) -> int:
        n = len(sentence)
        dictionary = set(dictionary)
        dp = [0]*(n+1)
        for i in range(1, n+1):
            dp[i] = dp[i-1]+1
            for j in range(i):
                if sentence[i-j-1:i] in dictionary:
                    dp[i] = min(dp[i],dp[i-j-1])
        return dp[n]
```

但只用哈希的话这题意思不大，加Trie优化后本题才到一个比较理想的性能：

```python
#Trie 单词最优匹配
class Trie:
    def __init__(self):
        self.root = {}
        self.word_end = -1
    
    def insert(self, word):
        curNode = self.root

        # 将单词逆序构建
        for c in word[::-1]:
            if c not in curNode:
                curNode[c] = {}
            curNode = curNode[c]
        
        curNode[self.word_end] = True


class Solution:
    def respace(self, dictionary: List[str], sentence: str) -> int:
        n, t = len(sentence), Trie()
        for word in dictionary:
            t.insert(word)
        dp = [0]*(n+1)
        for i in range(1,n+1):
            dp[i] = dp[i-1]+1
            node = t.root
            for j in range(i):
                c = sentence[i-j-1]
                if c not in node:
                    break
                elif t.word_end in node[c]:
                    dp[i] = min(dp[i],dp[i-j-1])
                node = node[c]
        return dp[n]
```



## 图

### 单源最短路径

Dijkstra算法

下面这道题就是变形，只不过改成了乘法概率最大，那么取个对数就是Dijkstra模板。所以不取对数，直接累乘当然可以，精度更高。

```python
#T1514 概率最大的路径
class Solution:
    def maxProbability(self, n: int, edges: List[List[int]], succProb: List[float], start: int, end: int) -> float:
        graph = collections.defaultdict(list)
        for i, (x, y) in enumerate(edges):
            graph[x].append((succProb[i], y))
            graph[y].append((succProb[i], x))
        
        que = [(-1.0, start)]
        prob = [0.0] * n
        prob[start] = 1.0

        while que:
            pr, node = heapq.heappop(que)
            pr = -pr
            if pr < prob[node]:
                continue
            for prNext, nodeNext in graph[node]:
                if prob[nodeNext] < prob[node] * prNext:
                    prob[nodeNext] = prob[node] * prNext
                    heapq.heappush(que, (-prob[nodeNext], nodeNext))
        
        return prob[end]
```



## 数学

### Catalan数

T96不同的二叉搜索树

```python
#不同的二叉搜索树
class Solution:
    def numTrees(self, n: int) -> int:
        ans = 1
        for i in range(2,n+1):
            ans = ans*(4*i-2)//(i+1)
        return ans
```



## 轮子库

### GCD

```python
#GCD
def gcd(a:int,b:int)->int:
	return gcd(b,a%b) if b else a
```



### 双指针

快慢指针：

O(1)空间复杂度不改变链表索引查询链表是否有环

```python
#T141 环形链表
# Definition for singly-linked list.
# class ListNode:
#     def __init__(self, x):
#         self.val = x
#         self.next = None

class Solution:
    def hasCycle(self, head: ListNode) -> bool:
        if not head or not head.next:
            return False
        slow = head
        fast = head.next
        while slow != fast:
            if not fast or not fast.next:
                return False
            slow = slow.next
            fast = fast.next.next
        return True
```

经典的翻转链表：

```java
//翻转链表
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
#斐波那契数列（矩阵快速幂）
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
#求数组中的两个不同元素（求一个不同元素的变化，位运算）
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

### 高精度乘法

真python式写法：str(int(num1)*int(num2))

假python式写法

```python
class Solution:
    def multiply(self, num1: str, num2: str) -> str:

        a = num1[::-1]
        b = num2[::-1]
        res = 0

        for i, x in enumerate(b):
            temp_res = 0
            for j, y in enumerate(a):
                temp_res += int(x) * int(y) * 10 ** j
            res += temp_res * 10 ** i

        return str(res)
```

C式python写法

```python
class Solution:
    def multiply(self, num1: str, num2: str) -> str:
        if num1 == '0' or num2 =='0':
            return '0'
        def chr2num(c:chr)->int:
            return ord(c)-ord('0')
        len1, len2 = len(num1), len(num2)
        ans = [0 for i in range(len1+len2)]
        for i in range(len1):
            for j in range(len2):
                ans[i+j] += chr2num(num1[len1-i-1])*chr2num(num2[len2-j-1])
        for i in range(len1+len2):
            if ans[i]>=10:
                ans[i+1]+=ans[i]//10
                ans[i] = ans[i]%10
        ans.reverse()
        if ans[0]==0:
            ans.remove(ans[0])
        for i in range(len(ans)):
            ans[i] = chr(ans[i]+48)
        return "".join(ans)
```

卷积大法（补：FFT？？？:)  ）

```python
#Copyright by Sx
import numpy as np
class Solution:
    def multiply(self, num1: str, num2: str) -> str:
        if num1=='0' or num2 == '0':
            return '0'
        num1, num2 = list(num1), list(num2)
        n1 = [int(num1[i]) for i in range(len(num1))]
        n2 = [int(num2[i]) for i in range(len(num2))]
        n = np.convolve(n1,n2,'full')
        n = list(n)
        for i in range(len(n)-1,0,-1):
            n[i-1]+=n[i]//10
            n[i] = n[i]%10
        if n[0]>10:
            tmp = n[0]//10
            n[0] = n[0]%10
            n.insert(0,tmp)
        while n[0] == 0:
            n.remove(0)
            if len(n)==1:
                break
        ans = [str(n[i]) for i in range(len(n))]
        return "".join(ans)
```

最后是FFT版的

```c++
//Copyright by unkown others, using C++ language
class Solution {
public:
    using CP = complex <double>;
    
    static constexpr int MAX_N = 256 + 5;

    double PI;
    int n, aSz, bSz;
    CP a[MAX_N], b[MAX_N], omg[MAX_N], inv[MAX_N];

    void init() {
        PI = acos(-1);
        for (int i = 0; i < n; ++i) {
            omg[i] = CP(cos(2 * PI * i / n), sin(2 * PI * i / n));
            inv[i] = conj(omg[i]);
        }
    }

    void fft(CP *a, CP *omg) {
        int lim = 0;
        while ((1 << lim) < n) ++lim;
        for (int i = 0; i < n; ++i) {
            int t = 0;
            for (int j = 0; j < lim; ++j) {
                if((i >> j) & 1) t |= (1 << (lim - j - 1));
            }
            if (i < t) swap(a[i], a[t]);
        }
        for (int l = 2; l <= n; l <<= 1) {
            int m = l / 2;
            for (CP *p = a; p != a + n; p += l) {
                for (int i = 0; i < m; ++i) {
                    CP t = omg[n / l * i] * p[i + m];
                    p[i + m] = p[i] - t;
                    p[i] += t;
                }
            }
        }
    }

    string run() {
        n = 1;
        while (n < aSz + bSz) n <<= 1;
        init();
        fft(a, omg);
        fft(b, omg);
        for (int i = 0; i < n; ++i) a[i] *= b[i];
        fft(a, inv);
        int len = aSz + bSz - 1;
        vector <int> ans;
        for (int i = 0; i < len; ++i) {
            ans.push_back(int(round(a[i].real() / n)));
        }
        // 处理进位
        int carry = 0;
        for (int i = ans.size() - 1; i >= 0; --i) {
            ans[i] += carry;
            carry = ans[i] / 10;
            ans[i] %= 10;
        }
        string ret;
        if (carry) {
            ret += to_string(carry);
        }
        for (int i = 0; i < ans.size(); ++i) {
            ret.push_back(ans[i] + '0');
        }
        // 处理前导零
        int zeroPtr = 0;
        while (zeroPtr < ret.size() - 1 && ret[zeroPtr] == '0') ++zeroPtr;
        return ret.substr(zeroPtr, INT_MAX);
    }

    string multiply(string num1, string num2) {
        aSz = num1.size();
        bSz = num2.size();
        for (int i = 0; i < aSz; ++i) a[i].real(num1[i] - '0');
        for (int i = 0; i < bSz; ++i) b[i].real(num2[i] - '0');
        return run();
    }
};
```

