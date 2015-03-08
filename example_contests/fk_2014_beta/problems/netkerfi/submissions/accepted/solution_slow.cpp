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
    int n, m;
    scanf("%d %d\n", &n, &m);

    vi *adj = new vi[n];

    for (int i = 0; i < m; i++)
    {
        int x, y;
        scanf("%d %d\n", &x, &y);
        x--, y--;

        adj[x].push_back(y);
        adj[y].push_back(x);
    }

    bool *visited = new bool[n];

    bool any = false;

    for (int i = 0; i < n; i++)
    {
        memset(visited, 0, n);

        stack<int> S;
        S.push(i);
        bool found = false;
        visited[i] = true;

        while (!S.empty())
        {
            int cur = S.top(); S.pop();
            if (cur == 0)
            {
                found = true;
                break;
            }

            for (int j = 0; j < size(adj[cur]); j++)
            {
                int nxt = adj[cur][j];
                if (!visited[nxt])
                {
                    visited[nxt] = true;
                    S.push(nxt);
                }
            }
        }

        if (!found)
        {
            printf("%d\n", i + 1);
            any = true;
        }
    }

    if (!any)
    {
        printf("Allir nettengdir\n");
    }

    delete[] visited;
    delete[] adj;

    return 0;
}

