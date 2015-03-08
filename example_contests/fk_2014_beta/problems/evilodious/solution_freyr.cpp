#include <iostream>
#include <map>

using namespace std;

typedef unsigned long long ull;

map<ull,ull> oNrs;
map<ull,ull> eNrs;
map<ull,ull>::iterator it;

ull odious(ull n)
{
    if (n < 2) return 1;
    it = oNrs.find(n);
    if (it != oNrs.end()) return it->second;

    ull ret;
    if (n % 2) ret = odious((n+1)/2) + n-1;
    else ret = 3*(n-1) - odious(n/2);

    oNrs.insert(make_pair<ull,ull>(n,ret));
    return ret;
}

ull evil(ull n)
{
    if (n < 2) return 0;
    it = eNrs.find(n);
    if (it != eNrs.end()) return it->second;

    ull ret;
    if (n % 2) ret = evil((n+1)/2)+n-1;
    else ret = 3*(n-1) - evil(n/2);

    eNrs.insert(make_pair<ull,ull>(n,ret));
    return ret;
}

int main()
{
    ull n;
    cin >> n;

    cout << odious(n) + evil(n) << endl;

    return 0;
}
