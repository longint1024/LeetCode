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