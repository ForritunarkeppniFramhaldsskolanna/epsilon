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

bool distinct(vi x)
{
    set<int> y(all(x));
    return size(x) == size(y);
}

int main()
{
    int board[9][9];
    for (int i = 0; i < 9 + 2; i++)
    {
        string line;
        getline(cin, line);
        for (int j = 0; j < 9 + 2; j++)
        {
            if (i % 4 != 3 && j % 4 != 3)
            {
                board[i - i/4][j - j/4] = line[j] - '0';
            }
        }
    }

    bool ok = true;

    for (int i = 0; i < 9; i++)
    {
        vi a, b;
        for (int j = 0; j < 9; j++)
        {
            a.push_back(board[i][j]);
            b.push_back(board[j][i]);
        }

        ok = ok && distinct(a);
        ok = ok && distinct(b);
    }

    for (int i = 0; i < 3; i++)
    {
        for (int j = 0; j < 3; j++)
        {
            vi c;
            for (int x = 0; x < 3; x++)
            {
                for (int y = 0; y < 3; y++)
                {
                    c.push_back(board[3*i+x][3*j+y]);
                }
            }

            ok = ok && distinct(c);
        }
    }

    printf("%s\n", ok ? "Leyst" : "Ekki Leyst");

    return 0;
}

