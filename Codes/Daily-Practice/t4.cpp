class Solution {
public:
    double findMedianSortedArrays(vector<int>& nums1, vector<int>& nums2) {
        int len1=nums1.size();
        int len2=nums2.size();
        int point1=0,point2=0;
        int maxlongint=2147483600;
        double ans;
        int len=len1+len2;
        int tot=0;
        if(len1==0||len2==0)
        {
            if(len1==0)
            {
                if(len2&1==1)ans=nums2[len2/2];
                else ans=double(nums2[len2/2-1]+nums2[len2/2])/2;
            }
            else
            {
                if(len1&1==1)ans=nums1[len1/2];
                else ans=double(nums1[len1/2-1]+nums1[len1/2])/2;
            }
        }
        else
        {
        if(len&1==1)
        {
            int index=len/2;
            while(1)
            {
                if(tot==index)
                {
                    ans=min(nums1[point1],nums2[point2]);
                    break;
                }
                else
                {
                    if(nums1[point1]<nums2[point2])
                    {
                        if(point1<len1-1)point1++;
                        else nums1[point1]=maxlongint;
                    }
                    else 
                    {
                        if(point2<len2-1)point2++;
                        else nums2[point2]=maxlongint;
                    }
                }
                tot++;
            }
        }
        else
        {
            int index1=(len-1)/2;
            int index2=len/2;
            while(1)
            {
                if(tot==index2)
                {
                    ans=double(ans+min(nums1[point1],nums2[point2]))/2;
                    break;
                }
                else
                {
                    if(tot==index1)
                    {
                        ans=min(nums1[point1],nums2[point2]);
                    }
                    if(nums1[point1]<nums2[point2])
                    {
                        if(point1<len1-1)point1++;
                        else nums1[point1]=maxlongint;
                    }
                    else 
                    {
                        if(point2<len2-1)point2++;
                        else nums2[point2]=maxlongint;
                    }
                }
                tot++;
            }
        }
        }
        return ans;
    }
};