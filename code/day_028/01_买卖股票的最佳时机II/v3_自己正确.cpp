class Solution {
public:
    int maxProfit(vector<int>& prices) {
        int sum=0;
        int Diff=0;

        for(int i=0; i<prices.size()-1; i++){
            Diff = prices[i+1]-prices[i];

            if(Diff>=0){
                sum += Diff;
            }

        }

        return sum;
    }
};