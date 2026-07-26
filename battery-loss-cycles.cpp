#include <bits/stdc++.h>
using namespace std;

double m_n_1, m_n, r_plus_n_1=1, r_minus_n_1=1, C_n, r_plus_n=1, r_minus_n=1;

const double M_Li = 6.94; // g/mol
const double V = 2.5e-7; // m^3
const double U0 = 3.7; // V
const double E_std = 3.0401; // V
const double F = 96485; // C/mol
const double R = 8.314; // J/(mol·K)
const double T = 298; // K
const double C_0 = 100; // mAh
const double m = 50; // g

int N;

int main ()
{
    freopen("battery-loss-output.csv", "w", stdout);
    cin >> N;
    m_n_1 = m;
    C_n = C_0;
    for (int i=1; i<=N; i++)
    {
        r_plus_n_1 = 1 - (M_Li * V / m_n_1) * exp(-F * (U0 - E_std) / (0.25 * R * T));
        r_minus_n_1 = 1 - (M_Li * V / m_n_1) * exp(-F * (5 - U0 + E_std) / (0.25 * R * T));
        m_n = m_n_1 * r_plus_n_1 * r_minus_n_1;
        C_n = C_n * r_plus_n_1 * r_minus_n_1;
        printf("%d,%.6f,%.6f,%.6f,%.6f\n", i, m_n, r_plus_n_1, r_minus_n_1, C_n);
        m_n_1 = m_n;
        C_n = C_n;
    }

    fclose(stdout);
    return 0;
}