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

ll cnt[70][2];

ll nth(int bs, ll n, bool even)
{
    ll res = 0;
    for (int i = bs; i > 0; i--)
    {
        res <<= 1;

        if (n >= cnt[i-1][even])
        {
            n -= cnt[i-1][even];
            res |= 1;
            even = !even;
        }
    }

    return res;
}

int main()
{
    for (int i = 0; i < 70; i++)
    {
        for (int j = 0; j < 2; j++)
        {
            if (i == 0)
            {
                cnt[i][j] = j == 1 ? 1 : 0;
            }
            else
            {
                cnt[i][j] = cnt[i-1][j] + cnt[i-1][!j];
            }
        }
    }

    ll n;
    cin >> n;
    n--;

    cout << nth(64, n, false) + nth(64, n, true) << endl;

    return 0;
}

