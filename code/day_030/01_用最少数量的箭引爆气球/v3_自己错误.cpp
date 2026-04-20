class Solution {
public:
    static bool cmp(vector<int> a, vector<int> b){
        return a[0] < b[0];
    }

    int findMinArrowShots(vector<vector<int>>& points) {
        int result=1;
        int start=0;

        sort(points.begin(), points.end(), cmp);

        for (const auto& p : points) {
            cout << "[" << p[0] << ", " << p[1] << "] ";
        }
        cout << endl;

        if(points.size() == 0) return 0;

        for(int i=1; i<points.size(); i++){
            if(points[i][0] <= points[i-1][1] && points[i][0] <= points[start][1]) {
                continue;
            } 
            start = i;
            result ++;
        }

        return result;
    }
};