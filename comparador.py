import subprocess
import time
import pandas as pd
import plotly.express as px
from jinja2 import Template

# Inputs

num_films = []
num_categories = []

# Le o tamando dos inputs
with open("inputs/sizes.txt", "r") as f: 
    lines = f.readlines()
    num_films = [int(n) for n in lines[0].strip().split(": ")[1].split(", ")]
    num_categories = [int(m) for m in lines[1].strip().split(": ")[1].split(", ")] 

# Armazena os tempos de execução e tempos de tela para cada heurística
greedy_times = {'num_films':[],'num_categories':[], 'execution': [], 'screen': []}
exploration_times = {'num_films':[],'num_categories':[],'execution': [], 'screen': []}

# Executa as duas heuristicas para cada input
for n in num_films:
    for m in num_categories:
        greedy_times['num_films'].append(n)
        greedy_times['num_categories'].append(m)
        exploration_times['num_films'].append(n)
        exploration_times['num_categories'].append(m)

        print(f"Running input with {n} films and {m} categories...")
        input_file = f"inputs/input_{n}_{m}.txt"

        start_time = time.time()
        output = subprocess.check_output(['./gulosa', input_file])
        end_time = time.time()

        # Armazena o tempo de execução
        greedy_times['execution'].append(end_time - start_time)
        
        # Calcula o tempo de tela
        max_screen_time = 0
        current_screen_time = 0
        movies = output.decode().strip().split('\n')[1:]
        for movie in movies:
            start, end, _ = map(int, movie.split())
            if start >= current_screen_time:
                current_screen_time = end
                screen_time = end - start
                if screen_time > max_screen_time:
                    max_screen_time = screen_time
        
        # Armazena o tempo de tela
        greedy_times['screen'].append(max_screen_time)
        
        start_time = time.time()
        output = subprocess.check_output(['./aleatoria', input_file])
        end_time = time.time()
        exploration_times['execution'].append(end_time - start_time )

            # Calcula o tempo de tela
        max_screen_time = 0
        current_screen_time = 0
        movies = output.decode().strip().split('\n')[1:]
        for movie in movies:
            start, end, _ = map(int, movie.split())
            if start >= current_screen_time:
                current_screen_time = end
                screen_time = end - start
                if screen_time > max_screen_time:
                    max_screen_time = screen_time
        
        # Armazena o tempo de tela
        exploration_times['screen'].append(max_screen_time)

        
# Cria dataframes
df_greedy = pd.DataFrame({
    'num_films': greedy_times['num_films'],
    'num_categories': greedy_times['num_categories'],
    'execution_time': greedy_times['execution'],
    'screen_time': greedy_times['screen']
})
df_exploration = pd.DataFrame({
    'num_films': exploration_times['num_films'],
    'num_categories': exploration_times['num_categories'],
    'execution_time': exploration_times['execution'],
    'screen_time': exploration_times['screen']
})


# Cria gráfico de tempo de execução em função do número de filmes
fig1 = px.line(df_greedy, x="num_films", y="execution_time", color="num_categories", 
                title="Tempo de Execução x Numero de Filmes - Greedy Heuristic",
                labels={"num_films": "Número de Filmes", "execution_time": "Tempo de Execução (s)"})
fig2 = px.line(df_exploration, x="num_films", y="execution_time", color="num_categories", 
                title="Tempo de Execução x Numero de Filmes - Exploration Heuristic",
                labels={"num_films": "Número de Filmes", "execution_time": "Tempo de Execução (s)"})

# Cria gráfico de tempo de execução em função do número de categorias
fig3 = px.line(df_greedy, x="num_categories", y="execution_time", color="num_films", 
                title="Tempo de Execução x Numero de Categorias - Greedy Heuristic",
                labels={"num_categories": "Número de Categorias", "execution_time": "Tempo de Execução (s)"})
fig4 = px.line(df_exploration, x="num_categories", y="execution_time", color="num_films", 
                title="Tempo de Execução x Numero de Categorias - Exploration Heuristic",
                labels={"num_categories": "Número de Categorias", "execution_time": "Tempo de Execução (s)"})

# Cria gráfico de tempo de tela em função do número de filmes
fig5 = px.line(df_greedy, x="num_films", y="screen_time", color="num_categories",
                title="Tempo de Tela x Numero de Filmes - Greedy Heuristic",
                labels={"num_films": "Número de Filmes", "screen_time": "Tempo de Tela (h)"})
fig6 = px.line(df_exploration, x="num_films", y="screen_time", color="num_categories",
                title="Tempo de Tela x Numero de Filmes - Exploration Heuristic",
                labels={"num_films": "Número de Filmes", "screen_time": "Tempo de Tela (h)"})

# Cria gráfico de tempo de tela em função do número de categorias
fig7 = px.line(df_greedy, x="num_categories", y="screen_time", color="num_films",
                title="Tempo de Tela x Numero de Categorias- Greedy Heuristic",
                labels={"num_categories": "Número de Categorias", "screen_time": "Tempo de Tela (h)"})
fig8 = px.line(df_exploration, x="num_categories", y="screen_time", color="num_films",
                title="Tempo de Tela x Numero de Categorias - Exploration Heuristic",
                labels={"num_categories": "Número de Categorias", "screen_time": "Tempo de Tela (h)"})

# Render Jinja2 template with plotly figures
template = Template("""
<!DOCTYPE html>
<html>
<head>
    <title>Movie Selection Heuristics Comparison</title>
    <script src="https://cdn.plot.ly/plotly-latest.min.js"></script>
</head>
<body>
<div class="text-section">
    <h1>Maratona de Filmes</h1>
    <h2>Heurística 1: Greedy</h2>
    <div style="font-size: 25px;">
    <p>
    A heurística Gulosa utiliza uma abordagem simples para o problema, de maneira gulosa, pois ela irá sempre 
    adicionar o filme com maior valor de horas, na categoria com maior numero de filmes permitidos. Nessa sequencia
    a heurística preenche a lista de filmes sem preocupacao com o tempo total de tela, e sim com a adicao do maior
    numero de horas o mais rapido possivel
    <p><p>
    A implementacão dessa heurística é simples, os dados são lidos a partir de um arquivo e texto, onde no
    cabecalho temos o numero de filmes e de categorias, e os filmes permitidos por categoria. Os dados dos filmes
    são armazenados em um Struct Filme. Ordenamos os filmes pela hora do seu término e salvamos no mesmo vetor
    <p><p>
    O filme é selcionado com criterio de não ter conflito com nenhum filme ja escolhido, e ser o filme com a maior
    duração disponível para a categoria. Os filmes selecionados são salvos em um Struct, e quando o programa termina
    o numero de filmes selecionados é imprimido no terminal, seguido pelas informacões de cada filme selcionado.
    O total de horas é calculado no programa de comparacão.
    <p><p>
    Essa heurística tem como inavariante o fato de que nenhum filme pode ser selcionado duas vezes, e que 
    sempre iremos selecionar primeiro o filme com maior duracão.
    <p>
    </div>
    

    <h2>Heurística 2: Greedy com 25% de aleatoriedade</h2>

    <div style="font-size: 25px;">
    <p>
    A segunda heurística é uma variação da heurística Gulosa. A aleatoriedade é introduzida para garantir um melhor resultado.
    Para isso, todo vez que é feita a escolha de um filme, há uma chance de 25% de um filme aleatório da lista ser escolhido,
    assim o tempo de tela e de execucão podem ser otimizados.
    <p><p>
    o restante da heurística segue o padrão da Gulosa. Para implementar a aleatoriedade, foi usado um fator de 25% de chance para
    ser escolhido um filme aleatoriamente ou não.
    <p><p>
    Temos as mesmas inavariantes da Gulosa, porem adicionamos a chance de um filme ser escolhido aleatoriamente com 25% de chance.
    <p>
    </div>
</div>
    <h1>Comparacão</h1>
    <h2>Tempo de Execução</h2>
    {{ fig1|safe }}
    {{ fig2|safe }}
    {{ fig3|safe }}
    {{ fig4|safe }}
    <h2>Tempo de Tela</h2>
    {{ fig5|safe }}
    {{ fig6|safe }}
    {{ fig7|safe }}
    {{ fig8|safe }}
</body>
</html>
""")

html = template.render(fig1=fig1.to_html(full_html=False), fig2=fig2.to_html(full_html=False),
                       fig3=fig3.to_html(full_html=False), fig4=fig4.to_html(full_html=False),
                       fig5=fig5.to_html(full_html=False), fig6=fig6.to_html(full_html=False),
                       fig7=fig7.to_html(full_html=False), fig8=fig8.to_html(full_html=False))

# Write HTML to file
with open("output.html", "w") as f:
    f.write(html)
