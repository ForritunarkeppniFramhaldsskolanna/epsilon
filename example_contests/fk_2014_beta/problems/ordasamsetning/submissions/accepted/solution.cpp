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
    string a, b;
    getline(cin, a);
    getline(cin, b);

    for (int len = min(size(a), size(b)); len >= 0; len--)
    {
        bool ok = true;

        for (int i = 0; ok && i < len; i++)
        {
            ok = a[size(a) - len + i] == b[i];
        }

        if (ok)
        {
            cout << a;
            for (int i = len; i < size(b); i++)
            {
                cout << b[i];
            }

            cout << endl;
            break;
        }
    }

    return 0;
}

