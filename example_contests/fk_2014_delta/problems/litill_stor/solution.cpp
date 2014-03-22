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
    string line;
    getline(cin, line);

    for (int i = 0; i < size(line); i++)
    {
        if (line[i] >= 'a' && line[i] <= 'z')
        {
            cout << static_cast<char>(line[i] - 'a' + 'A');
        }
        else if (line[i] >= 'A' && line[i] <= 'Z')
        {
            cout << static_cast<char>(line[i] - 'A' + 'a');
        }
        else
        {
            cout << line[i];
        }
    }

    cout << endl;

    return 0;
}

