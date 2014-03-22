#include<iostream>
using namespace std;

string s;
int at;

void output()
{
    int len = 0;
    bool first = true;

    switch (s[at])
    {
        case 'i':

            at++;
            while (s[at] != 'e')
            {
                cout << s[at];
                at++;
            }

            at++;

            break;

        case '0':
        case '1':
        case '2':
        case '3':
        case '4':
        case '5':
        case '6':
        case '7':
        case '8':
        case '9':

            while (s[at] != ':')
            {
                len = len * 10 + (s[at] - '0');
                at++;
            }

            at++;

            cout << "\"";
            for (int i = 0; i < len; i++)
            {
                cout << s[at];
                at++;
            }

            cout << "\"";

            break;

        case 'l':

            at++;
            cout << "[";

            while (s[at] != 'e')
            {
                if (first) first = false;
                else cout << ",";
                output();
            }

            at++;
            cout << "]";

            break;

        case 'd':

            at++;
            cout << "{";

            while (s[at] != 'e')
            {
                if (first) first = false;
                else cout << ",";
                output();
                cout << ":";
                output();
            }

            at++;
            cout << "}";

            break;
    }
}

int main()
{
    getline(cin, s);
    at = 0;
    output();
    cout << endl;
    return 0;
}

