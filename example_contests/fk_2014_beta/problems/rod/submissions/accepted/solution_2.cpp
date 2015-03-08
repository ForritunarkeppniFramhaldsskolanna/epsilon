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

    int **step = new int*[m];
    for (int i = 0; i < m; i++)
    {
        step[i] = new int[n];
        memset(step[i], 0, n << 2);
    }

    for (int i = 0; i < m; i++)
    {
        string line;
        getline(cin, line);

        for (int j = 0; j < n; j++)
        {
            if (2*j-1 >= 0 && line[2*j-1] == '-') assert(step[i][j] == 0), step[i][j] = -1;
            if (2*j+1 < size(line) && line[2*j+1] == '-') assert(step[i][j] == 0), step[i][j] = 1;
        }
    }

    char *res = new char[n];
    for (int i = 0; i < n; i++)
    {
        int at = i;
        for (int r = 0; r < m; r++)
        {
            at += step[r][at];
        }

        res[at] = 'A' + i;
    }

    for (int i = 0; i < n; i++)
        printf("%c", res[i]);

    printf("\n");

    return 0;
}

