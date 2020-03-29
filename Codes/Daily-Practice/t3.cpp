class Solution {
public:
    int lengthOfLongestSubstring(string s) {
        int ans=0;
        int front=0;
        int rear=-1;
        int len=s.length();
        int hash[256];
        for (int i=0;i<256;i++)hash[i]=0;
        while(rear<len-1)
        {
            rear++;
            if(hash[s[rear]]==0)
            {
                hash[s[rear]]=1;
            }
            else
            {
                while(hash[s[rear]]==1)
                {
                    hash[s[front]]=0;
                    front++;
                }
                hash[s[rear]]=1;
            }
            int sublen=rear-front+1;
            if(sublen>ans)ans=sublen;
        }
        return(ans);
    }
};