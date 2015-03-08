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

vector<string> split(string s, char c)
{
    vector<string> res;
    stringstream ss;
    for (int i = 0; i < size(s); i++)
    {
        if (s[i] == c)
        {
            res.push_back(ss.str());
            ss.str("");
        }
        else
        {
            ss << s[i];
        }
    }

    res.push_back(ss.str());
    return res;
}

int main()
{
    string s;
    getline(cin, s);

    vector<string> a = split(s, '.');
    vector<string> b = split(s, ':');

    bool ipv4 = size(a) == 4;
    bool ipv6 = size(b) == 8;

    if (ipv4)
    {
        for (int i = 0; i < 4; i++)
        {
            int res = 0;
            ipv4 = ipv4 && size(a[i]) > 0 && size(a[i]) <= 3;
            for (int j = 0; j < size(a[i]); j++)
            {
                if ('0' <= a[i][j] && a[i][j] <= '9')
                {
                    res = res * 10 + (a[i][j] - '0');
                }
                else
                {
                    ipv4 = false;
                    break;
                }
            }

            if (size(a[i]) > 1 && a[i][0] == '0')
            {
                ipv4 = false;
            }

            ipv4 = ipv4 && 0 <= res && res < 256;
        }
    }

    if (ipv6)
    {
        for (int i = 0; i < 8; i++)
        {
            ipv6 = ipv6 && size(b[i]) == 4;
            for (int j = 0; j < size(b[i]); j++)
            {
                if ('0' <= b[i][j] && b[i][j] <= '9') { }
                else if ('a' <= b[i][j] && b[i][j] <= 'f') { }
                else
                {
                    ipv6 = false;
                    break;
                }
            }
        }
    }

    if (ipv4)
    {
        printf("IPv4\n");
    }
    else if (ipv6)
    {
        printf("IPv6\n");
    }
    else
    {
        printf("Error\n");
    }

    return 0;
}

