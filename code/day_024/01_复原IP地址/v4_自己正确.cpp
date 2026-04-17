class Solution {
public:
    vector<string> result;
    string s_all;

    void backtracking(string s, int startIndex, int depth){
        if(depth >= 3){
            string s_new = s.substr(startIndex, s.size()-startIndex);
            if(isValid(s_new)){
                s_all += s_new;
                result.push_back(s_all);
                for(int k = 0; k < s_new.size(); k++){
                    s_all.pop_back();
                }
            }

            return ;

        } else{
            for(int i=startIndex; i<s.size() && i<startIndex+3; i++){

                string s_new = s.substr(startIndex, i-startIndex+1);
                
                if(isValid(s_new)){
                    s_all += s_new;
                    s_all += '.';
                } else{
                    continue;
                }
                backtracking(s, i+1, depth+1);
                int delete_len = s_new.size() + (depth < 4 ? 1 : 0);
                for(int k = 0; k < delete_len; k++){
                    s_all.pop_back();
                }
            }
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