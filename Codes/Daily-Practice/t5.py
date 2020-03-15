class Solution:
    def longestPalindrome(self, s: str) -> str:
        index_front=1
        index_tail=1
        maxlen=0
        for i in range(len(s)):
            if(i+1< len(s) and s[i] == s[i+1]):
                front = i
                tail = i+1
                while(front>0 and tail<len(s)-1):
                    if(s[front-1]==s[tail+1]):
                        front, tail = front-1, tail+1
                    else:
                        break
                len_tmp = tail-front+1
                if len_tmp>maxlen :
                    index_front, index_tail, maxlen = front, tail, len_tmp
            front=i
            tail=i
            while(front>0 and tail<len(s)-1):
                if(s[front-1]==s[tail+1]):
                    front, tail = front-1, tail+1
                else:
                    break
            len_tmp = tail-front+1
            if len_tmp>maxlen :
                index_front, index_tail, maxlen = front, tail, len_tmp
        return(s[index_front:index_tail+1])