class Solution {
public:
    vector<int> twoSum(vector<int>& nums, int target) {
        int index1,index2;
        for(int i=0;i<nums.size();i++){
            for (int j=i+1;j<nums.size();j++){
                if(nums[i]+nums[j]==target){
                    index1=i;
                    index2=j;
                    break;
                }
            }
        }
        vector<int> temp;
        temp.push_back(index1);
        temp.push_back(index2);
        return temp;
    }
};