#include <iostream>
#include <algorithm>
#include <vector>
#include <fstream>
#include <omp.h>

using namespace std;

struct Filme {
    int inicio, fim, categoria;
};

bool verificaConflito(Filme a, Filme b) {
    return a.inicio < b.fim && b.inicio < a.fim;
}

int main(int argc, char* argv[]) {
    if (argc != 2) {
        std::cerr << "Usage: " << argv[0] << " <input_file>\n";
        return 1;
    }

    ifstream input_file(argv[1]);
    if (!input_file.is_open()) {
        std::cerr << "Error: Failed to open input file: " << argv[1] << "\n";
        return 1;
    }

    int n, m;
    input_file >> n >> m;

    vector<int> max_filmes(m);
    for (int i = 0; i < m; i++) {
        input_file >> max_filmes[i];
    }

    vector<Filme> filmes(n);
    for (int i = 0; i < n; i++) {
        input_file >> filmes[i].inicio >> filmes[i].fim >> filmes[i].categoria;
    }

    input_file.close();

    int count = 0;
#pragma omp parallel for shared(count)
    for (int i = 0; i < n; i++) {
        int local_count = 0;
        for (int j = 0; j < n; j++) {
            if (i != j && filmes[i].categoria == filmes[j].categoria && verificaConflito(filmes[i], filmes[j])) {
                local_count++;
                if (local_count >= max_filmes[filmes[i].categoria - 1]) {
                    break;
                }
            }
        }
#pragma omp critical
        {
            if (local_count < max_filmes[filmes[i].categoria - 1]) {
                count++;
            }
        }
    }

    cout << count << endl;

    return 0;
}
