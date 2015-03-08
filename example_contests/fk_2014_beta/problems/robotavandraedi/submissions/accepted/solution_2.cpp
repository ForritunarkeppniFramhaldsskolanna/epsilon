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

    queue<ii> Q;

    char **arr = new char*[n];
    for (int i = 0; i < n; i++)
    {
        arr[i] = new char[m];
        for (int j = 0; j < m; j++)
        {
            scanf("%c", arr[i] + j);
            if (arr[i][j] == 'X')
            {
                Q.push(ii(i, j));
                arr[i][j] = '%';
            }
        }

        scanf("\n");
    }

    bool reached_border = false;
    while (!Q.empty())
    {
        ii cur = Q.front(); Q.pop();

        if (cur.first == 0 || cur.second == 0 || cur.first == n - 1 || cur.second == m - 1)
        {
            reached_border = true;
            break;
        }

        for (int di = -1; di <= 1; di++)
        {
            for (int dj = -1; dj <= 1; dj++)
            {
                if ((di == 0) ^ (dj == 0))
                {
                    int ci = cur.first + di,
                        cj = cur.second + dj;

                    if (ci >= 0 && cj >= 0 && ci < n && cj < m && arr[ci][cj] == '.')
                    {
                        arr[ci][cj] = '%';
                        Q.push(ii(ci, cj));
                    }
                }
            }
        }
    }

    if (reached_border)
    {
        printf("Death to humans\n");
    }
    else
    {
        printf("We are safe\n");
    }

    for (int i = 0; i < n; i++)
        delete[] arr[i];

    delete[] arr;

    return 0;
}

