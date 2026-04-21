#include <bits/stdc++.h>
using namespace std;

class Solution {
private:
    int M, N;
    vector<vector<int>> dp; // M行, N + 1列

public:
    Solution(int m, int n) : M(m), N(n), dp(m, vector<int>(n + 1, 0)) {}

    int maxValue(const vector<int>& space, const vector<int>& value) {
        // 0,1背包问题: 选与不选

        // 1. 确定dp数组: dp[i][j]代表行李箱空间为j的情况下,从下标为[0, i]的物品里面任意取,能达到的最大价值
        // vector<vector<int>> dp(space.size(), vector<int>(n + 1, 0));

        // 2. 初始化dp数组
        for (int j = space[0]; j <= N; ++j) {
            dp[0][j] = value[0];
        }
        
        // 3. 确定递推公式
        for (int i = 1; i < M; ++i) {
            for (int j = 1; j <= N; ++j) {
                if (j < space[i]) {
                    dp[i][j] = dp[i - 1][j];
                }
                else {
                    dp[i][j] = max(dp[i - 1][j], dp[i - 1][j - space[i]] + value[i]);
                    
                }
            }
        }
        return dp[M-1][N];

    }
    void printDP() {
        for (int i = 0; i < M; ++i) {
            for (int j = 0; j < N + 1; ++j) {
                cout << dp[i][j] << ' ';
            }
            cout << endl;
        }
    }

};

int main() {
    int m, n;
    cin >> m >> n; // 材料种类
    Solution s(m,n);

    vector<int> space(m, 0);
    vector<int> value(m, 0);
    for (int i = 0; i < m; ++i) {
        cin >> space[i];
    }
    for (int i = 0; i < m; ++i) {
        cin >> value[i];
    }
    
    int res = s.maxValue(space, value);
    //s.printDP();
    cout << res << endl;
    return 0;
}