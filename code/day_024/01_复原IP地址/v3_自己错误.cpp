class Solution {
public:
    vector<string> result;
    string s_all;

    void backtracking(string s, int startIndex, int depth){
        if(startIndex > s.size()-1){
            result.push_back(s_all);
            return ;
        }

        if(depth >= 3){
            string s_new = s.substr(startIndex, s.size()-startIndex);
            if(isValid(s_new)){
                s_all += s_new;
            } else{
                return ;
            }
        } else{
            for(int i=startIndex; i<s.size() && i<startIndex+4; i++){

                string s_new = s.substr(startIndex, i-startIndex+1);
                
                if(isValid(s_new)){
                    s_all += s_new;
                    s_all += '.';
                } else{
                    continue;
                }
                backtracking(s, i+1, depth+1);
                for(int i=0; i<s_new.size()+1; i++){
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