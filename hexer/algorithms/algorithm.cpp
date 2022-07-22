#include <bits/stdc++.h>

using namespace std;

constexpr int max_n = 205;
constexpr int max_val = (1 << 14);
constexpr int INF = 1e9 + 7;

int n, m, p, k, q, r, bit_m, v, w, t, s, u, b, path;
bool ok = false;
int K[max_n];
vector<tuple<int, int, int>> G[max_n];

bool processed[max_n][max_val];
int dist[max_n][max_val];
priority_queue<tuple<int, int, int>> Q;

bool fight(int mask, int cost) {
    if (cost == 0) return true;
    for (int i = 1; i <= 13; i++) {
        if ((cost & (1 << i)) && !(mask & (1 << i))) { 
            return false;
        }
    }
    return true;
}

int main() {
    ios_base::sync_with_stdio(0);
    cin.tie(0);

    cin >> n >> m >> p >> k;
    for (int i = 0; i < k; i++) {
        cin >> w >> q;
        bit_m = K[w];
        for (int j = 0; j < q; j++) {
            cin >> r;
            bit_m |= (1 << r);
        }
        K[w] = bit_m;
    }

    for (int i = 0; i < m; i++) {
        cin >> v >> w >> t >> s;
        bit_m = 0;
        for (int j = 0; j < s; j++) {
            cin >> u;
            bit_m |= (1 << u);
        }
        G[v].push_back({w, t, bit_m});
        G[w].push_back({v, t, bit_m});
    }

    for (int j = 0; j < (1 << 14); j++)
        for (int i = 0; i <= n; i++) dist[i][j] = INF;

    bit_m = K[1];
    dist[1][bit_m] = 0;
    Q.push({0, 1, bit_m});

    while (!Q.empty()) {
        int d, a, current_mask;
        tie(d, a, current_mask) = Q.top(); Q.pop();
        if (processed[a][current_mask]) continue;
        if (a == n) {
            cout << -d;
            ok = true;
            break;
        }

        processed[a][current_mask] = true;

        for (auto e : G[a]) {
            tie (b, w, path) = e;
            int next_mask = current_mask;
            if (fight(next_mask, path)) {                 
                next_mask |= K[b];
                if (dist[a][current_mask] + w < dist[b][next_mask]) {
                    dist[b][next_mask] = dist[a][current_mask] + w;
                    Q.push({-dist[b][next_mask], b, next_mask});
                }
            }
        }
    }

    if (!ok) cout << -1;

    return 0;
}