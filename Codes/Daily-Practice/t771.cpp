class Solution {
public:
    int numJewelsInStones(string J, string S) {
        int small[26];
        int large[26];
        for (int i=0;i<26;i++){
            small[i]=0;
            large[i]=0;
        }
        int len=J.length();
        for (int i=0;i<len;i++){
            int index=J[i]-'a';
            if(index<0){
                index=index+32;
                large[index]=1;
            }
            else{
                small[index]=1;
            }
        }
        len=S.length();
        int ans=0;
        for (int i=0;i<len;i++)
        {
            int index=S[i]-'a';
            if(index<0){
                index=index+32;
                if(large[index]==1){
                    ans++;
                }
            }
            else{
                if(small[index]==1){
                    ans++;
                }
            }
        }
        return(ans);
    }
};