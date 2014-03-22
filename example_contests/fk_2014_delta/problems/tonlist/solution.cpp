#include <iostream>
#include <cstdio>
#include <string>
using namespace std;

bool match(string patt, string inp)
{
    int ind = 0;
    for(; ind < inp.size() && ind < patt.size() && patt[ind] != '*'; ind++) {
        if(patt[ind] != inp[ind]) {
            return false;
        }
    }
    if(ind == patt.size() - 1) {
        return true;
    }
    int pind = patt.size() - 1;
    int iind = inp.size() - 1;
    for(; iind >= 0 && pind > ind; iind--, pind--) {
        if(patt[pind] != inp[iind] || iind < ind) {
            return false;
        }
    }
    return true;
}

bool match2(string patt, string inp)
{
    size_t pos = patt.find("*");
    if(pos == string::npos) {
        return patt == inp;
    }
    string lef = patt.substr(0, pos);
    string right = patt.substr(pos + 1);
    return inp.find(lef) == 0 && inp.rfind(right) >= pos;
}

int main()
{
    string patt;
    getline(cin,patt);

    int n;
    scanf("%d\n", &n);

    while(n--) {
        string inp;
        getline(cin,inp);
        cout << "Passar";
        if(!match2(patt, inp)) {
            cout << " ekki";
        }
        cout << endl;
    }

    return 0;
}
