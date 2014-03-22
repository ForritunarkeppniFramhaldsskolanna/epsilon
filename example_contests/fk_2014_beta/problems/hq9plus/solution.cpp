#include <iostream>
#include <string>
using namespace std;

int main()
{
    string code;
    getline(cin, code);

    int counter = 0;
    for (int i = 0, cnt = code.size(); i < cnt; i++)
    {
        if (code[i] == '+')
        {
            counter++;
        }
    }

    cout << counter << endl;

    return 0;
}

