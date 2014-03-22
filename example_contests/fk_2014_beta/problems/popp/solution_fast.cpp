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
    int n;
    scanf("%d\n", &n);

    ii *ev = new ii[2*n];
    for (int i = 0; i < n; i++)
    {
        int a, b;
        scanf("%d %d\n", &a, &b);
        ev[2*i] = ii(a, 0);
        ev[2*i+1] = ii(a+b-1, 1);
    }

    sort(ev, ev + 2*n);

    int rt = 0,
        rc = 0;

    int cur = 0;

    for (int i = 0; i < 2*n; i++)
    {
        if (ev[i].second == 0)
        {
            cur++;
            if (cur > rc)
            {
                rc = cur;
                rt = ev[i].first;
            }
        }
        else
        {
            cur--;
        }
    }

    assert(cur == 0);

    printf("%d %d\n", rt, rc);

    return 0;
}

