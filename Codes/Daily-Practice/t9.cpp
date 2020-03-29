class Solution {
public:
    bool isPalindrome(int x) {
        if(x<0)return false;
        else
        {
            long long y=x;
            long long t=0;
            while(y>0)
            {
                t=t*10+y%10;
                y=y/10;
            }
            y=x;
            if(t==y)return true;
            else return false;
        }
    }
};