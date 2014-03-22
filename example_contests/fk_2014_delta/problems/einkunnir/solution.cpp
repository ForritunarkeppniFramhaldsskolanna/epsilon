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
    cin >> n;

    map<string, int> cnt;
    map<string, double> sum;

    string s;
    double x;
    for (int i = 0; i < n; i++)
    {
        cin >> s >> x;
        s = s.substr(0, 3);
        cnt[s]++;
        sum[s] += x;
    }

    for (map<string, int>::const_iterator it = cnt.begin(); it != cnt.end(); ++it)
    {
        cout << it->first << " " << sum[it->first] / cnt[it->first] << endl;
    }

    return 0;
}

