#include <bits/stdc++.h>
using namespace std;

struct Filme { // Estrutura para armazenar os dados de cada filme
    int inicio, fim, categoria;
};

bool cmp_filmes(Filme a, Filme b) {
    return a.fim < b.fim; // Ordena por fim em ordem crescente
}

int main(int argc, char* argv[]) { // Recebe o nome do arquivo como parâmetro   
    if (argc != 2)
    {
        std::cerr << "Usage: " << argv[0] << " <input_file>\n"; // Exibe mensagem de erro
        return 1;
    }

    ifstream input_file(argv[1]); // Abre o arquivo
    if (!input_file.is_open())
    {
        std::cerr << "Error: Failed to open input file: " << argv[1] << "\n"; // Exibe mensagem de erro
        return 1;
    }

    int n, m; // n = número de filmes, m = número de categorias
    input_file >> n >> m; // Lê o número de filmes e o número de categorias

    vector<int> max_filmes(m); // Vetor com o máximo de filmes de cada categoria
    for(int i=0; i<m; i++) {
        input_file >> max_filmes[i];
    }

    vector<Filme> filmes(n); // Vetor com os filmes
    for(int i=0; i<n; i++) {
        input_file >> filmes[i].inicio >> filmes[i].fim >> filmes[i].categoria; // Lê o início, fim e categoria de cada filme
    }
    input_file.close();

    sort(filmes.begin(), filmes.end(), cmp_filmes); // Ordena por fim

    vector<int> selecionados(m, 0); 
    vector<Filme> solucao;

    for(int i=0; i<n; i++) {
        if(selecionados[filmes[i].categoria-1] < max_filmes[filmes[i].categoria-1]) { // Verifica se o filme selecionado não ultrapassa o máximo de filmes da categoria
            solucao.push_back(filmes[i]);
            selecionados[filmes[i].categoria-1]++;

            // 25% de chance de selecionar outro filme
            if(i+1 < n && (rand() % 4) == 0 && 
               filmes[i+1].inicio >= filmes[i].fim && 
               selecionados[filmes[i+1].categoria-1] < max_filmes[filmes[i+1].categoria-1]) { // Verifica se o próximo filme não ultrapassa o máximo de filmes da categoria
                solucao.push_back(filmes[i+1]);
                selecionados[filmes[i+1].categoria-1]++; 
                i++; // Pular para o próximo filme selecionado
            }
        }
    }

    cout << solucao.size() << endl;
    for(Filme f : solucao) {
        cout << f.inicio << " " << f.fim << " " << f.categoria << endl; // Imprime a solução
    }

    return 0;
}
