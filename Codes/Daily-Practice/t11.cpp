class Solution {
public:
    int maxArea(vector<int>& height) {
        int len=height.size();
        int index1=0;
        int index2=len-1;
        int ans=min(height[index1],height[index2])*(index2-index1);
        while(1)
        {
            if(height[index1]<height[index2])
            {
                while(height[index1+1]<height[index1])index1++;
                index1++;
            }
            else
            {
                while(height[index2-1]<height[index2])index2--;
                index2--;
            }
            int temp=min(height[index1],height[index2])*(index2-index1);
            if(temp>ans)ans=temp;
            if(index1>=index2)break;
        }
        return(ans);
    }
};