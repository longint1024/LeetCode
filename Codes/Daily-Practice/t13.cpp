class Solution {
public:
    int romanToInt(string s) {
        string sym[13]={"I","IV","V","IX","X","XL","L","XC","C","CD","D","CM","M"};
        int v[13]={1,4,5,9,10,40,50,90,100,400,500,900,1000};
        int index=0;
        int ans=0;
        int len=s.length();
        while(1)
        {
            bool ismatch=0;
            if(index>=len)break;
            if(index<len-1)
            {
                string temp={s[index],s[index+1]};
                for (int j=0;j<13;j++)
                    if(temp==sym[j])
                    {
                        ans=ans+v[j];
                        ismatch=1;
                        break;
                    }
            }
            if(ismatch){index=index+2;continue;}
            for (int j=0;j<13;j++)
                if(s[index]==sym[j][0]&&sym[j].length()==1)
                {
                    ans=ans+v[j];
                    index++;
                    break;
                }
        }
        return(ans);
    }
};