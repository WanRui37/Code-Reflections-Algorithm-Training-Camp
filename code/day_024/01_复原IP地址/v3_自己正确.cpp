class Solution {
public:
    vector<string> result;
    string s_all;

void backtracking(string& s, int startIndex, int depth){
    if(depth == 4){
        if(startIndex == s.size()){
            result.push_back(s_all);
        }
        return;
    }

    for(int i = startIndex; i < s.size() && i < startIndex + 3; i++){
        string s_new = s.substr(startIndex, i - startIndex + 1);

        if(!isValid(s_new)) continue;

        int len = s_all.size();

        s_all += s_new;
        if(depth < 3) s_all += '.';

        backtracking(s, i + 1, depth + 1);

        s_all.resize(len); // ⭐ 一步回溯（强烈推荐）
    }
}

    bool isValid(string s){
        if(s.size()>0 && s.size()<4 && std::stoi(s)>=0 && std::stoi(s)<=255){
            if(s.size()>1 && s[0]=='0'){
                return false;
            } 
            return true;
        } else{
            return false;
        }
    }

    vector<string> restoreIpAddresses(string s) {
        result.clear();
        backtracking(s, 0, 0);
        return result;
    }
};