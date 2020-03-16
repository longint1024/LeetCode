class Solution {
public:
    int reverse(int x) {
        long long maxlongint=2147483648;
        long long ans=0;
        int temp=x;
        long long y=x;
        if(y<0)y=-y;
        while(y>0)
        {
            ans=ans*10+y%10;
            y=y/10;
        }
        if(temp<0)ans=-ans;
        if(ans>maxlongint-1||ans<-maxlongint)ans=0;
        return(int(ans));
    }
};