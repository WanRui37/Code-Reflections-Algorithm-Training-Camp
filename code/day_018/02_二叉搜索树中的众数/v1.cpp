class Solution {
public:
    unordered_map<int, int> map;

    void traverse(TreeNode* node){
        if(node == NULL) return;
        traverse(node->left);
        map[node->val]++;  // 统计频率
        traverse(node->right);
    }

    vector<int> findMode(TreeNode* root) {
        map.clear();
        traverse(root);
        vector<int> result;
        
        // 第一步：找到最大出现次数
        int maxCount = 0;
        for(auto& p : map){
            if(p.second > maxCount){
                maxCount = p.second;
            }
        }
        
        // 第二步：把所有频率等于最大次数的数加入结果
        for(auto& p : map){
            if(p.second == maxCount){
                result.push_back(p.first);
            }
        }
        
        return result;
    }
};