class Solution {
public:
    string intToRoman(int num) {
        string s[13]={"I","IV","V","IX","X","XL","L","XC","C","CD","D","CM","M"};
        string ans="";
        int v[13]={1,4,5,9,10,40,50,90,100,400,500,900,1000};
        int temp=num;
        for (int i=12;i>=0;i--)
        {
            for(int j=0;j<temp/v[i];j++)ans=ans+s[i];
            temp=temp%v[i];
        }
        return(ans);
    }
};