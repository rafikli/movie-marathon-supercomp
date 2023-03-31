#include <iostream>
#include <algorithm>
#include <vector>
#include <fstream>
using namespace std;

struct Filme { // Estrutura para armazenar os dados de cada filme       
    int inicio, fim, categoria; 
};

bool cmp(Filme a, Filme b) {
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
    for (int i = 0; i < m; i++) { 
        input_file >> max_filmes[i];
    }

    vector<Filme> filmes(n); // Vetor com os filmes
    for (int i = 0; i < n; i++) {
        input_file >> filmes[i].inicio >> filmes[i].fim >> filmes[i].categoria; // Lê o início, fim e categoria de cada filme
    }

    input_file.close();
    
    sort(filmes.begin(), filmes.end(), cmp); // Ordena por fim

    int num_filmes = 0;
    vector<int> num_filmes_categoria(m, 0); // Vetor com o número de filmes em cada categoria
    vector<Filme> selecionados; // Vetor com os filmes selecionados

    for (int i = 0; i < n; i++) {
        if (num_filmes_categoria[filmes[i].categoria - 1] < max_filmes[filmes[i].categoria - 1]) {  // Verifica se o filme selecionado não ultrapassa o máximo de filmes da categoria
            bool conflito = false;
            for (int j = 0; j < selecionados.size(); j++) {
                if (filmes[i].inicio < selecionados[j].fim && filmes[i].fim > selecionados[j].inicio) {
                    conflito = true; // Verifica se o filme selecionado tem conflito com algum outro filme selecionado
                    break;
                }
            }
            if (!conflito) {
                num_filmes++;
                num_filmes_categoria[filmes[i].categoria - 1]++;
                selecionados.push_back(filmes[i]); // Adiciona o filme ao vetor de filmes selecionados
            }
        }
    }

    cout << num_filmes << endl;
    for (int i = 0; i < selecionados.size(); i++) {
        cout << selecionados[i].inicio << " " << selecionados[i].fim << " " << selecionados[i].categoria << endl; // Imprime os dados dos filmes selecionados
    }

    return 0;
}
