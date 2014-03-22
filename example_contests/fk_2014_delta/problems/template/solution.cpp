#include <algorithm>
#include <bitset>
#include <cassert>
#include <cmath>
#include <cstdio>
#include <cstdlib>
#include <cstring>
#include <ctime>
#include <fstream>
#include <iomanip>
#include <iostream>
#include <list>
#include <map>
#include <queue>
#include <set>
#include <sstream>
#include <stack>
#include <string>
#include <utility>
#include <vector>
using namespace std;

#define all(o) (o).begin(), (o).end()
#define allr(o) (o).rbegin(), (o).rend()
const int INF = 2147483647;
typedef long long ll;
typedef pair<int, int> ii;
typedef vector<int> vi;
typedef vector<ii> vii;
typedef vector<vi> vvi;
typedef vector<vii> vvii;
template <class T> int size(T &x) { return x.size(); }

// assert or gtfo

int main()
{
    map<string, string> info;

    string line;
    while (getline(cin, line) && line != "===")
    {
        stringstream ss;
        int at = 0;
        while (line[at] != '=')
        {
            ss << line[at];
            at++;
        }

        string key = ss.str();
        ss.str("");

        at++;
        while (at < size(line))
        {
            ss << line[at];
            at++;
        }

        string value = ss.str();
        info[key] = value;
    }

    while (getline(cin, line) && line != "===")
    {
        int at = 0;
        while (at < size(line))
        {
            if (line[at] == '{')
            {
                stringstream ss;
                at++;
                while (line[at] != '}')
                {
                    ss << line[at];
                    at++;
                }

                at++;
                cout << info[ss.str()];
            }
            else
            {
                cout << line[at];
                at++;
            }
        }

        cout << endl;
    }

    return 0;
}

