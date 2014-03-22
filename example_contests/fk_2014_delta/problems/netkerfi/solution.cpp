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

int *uf;

int find(int x)
{
    return uf[x] == x ? x : uf[x] = find(uf[x]);
}

int main()
{
    int n, m;
    scanf("%d %d\n", &n, &m);

    uf = new int[n];
    for (int i = 0; i < n; i++)
    {
        uf[i] = i;
    }

    for (int i = 0; i < m; i++)
    {
        int a, b;
        scanf("%d %d\n", &a, &b);
        a--, b--;

        uf[find(a)] = find(b);
    }

    bool any = false;

    for (int i = 0; i < n; i++)
    {
        if (find(i) != find(0))
        {
            printf("%d\n", i + 1);
            any = true;
        }
    }

    if (!any)
    {
        printf("Allir nettengdir\n");
    }

    delete[] uf;

    return 0;
}

