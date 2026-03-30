# 📐 Documentação Técnica - AdaLove Gestor de Notas

## 🏗️ Arquitetura da Solução

```
┌─────────────────────────────────────────────────────────┐
│                   CLIENTE (Streamlit)                   │
├─────────────────────────────────────────────────────────┤
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐  │
│  │   Interface  │  │   Gráficos   │  │   Editor     │  │
│  │   KPI        │  │  (Plotly)    │  │  Dados       │  │
│  └──────────────┘  └──────────────┘  └──────────────┘  │
├─────────────────────────────────────────────────────────┤
│              CAMADA DE PROCESSAMENTO                    │
├─────────────────────────────────────────────────────────┤
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐  │
│  │   Parsing    │  │   Cálculos   │  │   Validação  │  │
│  │   HTML       │  │  Ponderados  │  │   Dados      │  │
│  └──────────────┘  └──────────────┘  └──────────────┘  │
├─────────────────────────────────────────────────────────┤
│                 DADOS (Em Memória)                      │
├─────────────────────────────────────────────────────────┤
│  ┌──────────────────────────────────────────────────┐  │
│  │  DataFrame Pandas (Atividades com Notas)         │  │
│  │  Columns: Atividade, Status, Pontos, Nota, etc  │  │
│  └──────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────┘
```

## 📦 Componentes Principais

### 1. **Módulo de Parsing HTML**

```python
def parse_html_activities(html_path: str) -> pd.DataFrame
```

**Responsabilidades:**
- Ler arquivo HTML do AdaLove
- Localizar tabelas com class "styled-tr"
- Extrair dados de 5 colunas principais
- Tratar valores "-" como NaN (pendentes)
- Retornar DataFrame estruturado

**Fluxo:**
```
HTML Input
    ↓
BeautifulSoup Parse
    ↓
Find rows (class="styled-tr")
    ↓
Extract cells (5 colunas)
    ↓
Process types (float, bool)
    ↓
DataFrame Output
```

**Dados Extraídos:**
```
├─ Atividade (string): Nome da tarefa
├─ Status (string): Feito/Não Feito
├─ Pontos (float): Peso da atividade
├─ Nota (float): Nota obtida ou NaN
└─ Pendente (bool): Aguarda avaliação?
```

### 2. **Módulo de Cálculos**

#### 2.1 Média Ponderada
```python
def calculate_weighted_average(df: pd.DataFrame) -> tuple
```

**Algoritmo:**
```
1. Filtrar apenas linhas com Nota ≠ NaN
2. Se vazio → retornar (0.0, 0.0, total_pontos)
3. weighted_sum = Σ(Nota × Pontos)
4. total_points = Σ(Pontos) [apenas avaliadas]
5. average = weighted_sum / total_points
6. Retornar (average, total_pontos_avaliados, total_pontos_possíveis)
```

**Complexidade:** O(n) onde n = número de atividades

#### 2.2 Status de Aprovação
```python
def get_approval_status(average: float, threshold: float) -> str
```

**Lógica de Negócio:**
```
if average >= threshold:
    return "✅ Aprovado"
elif average >= 5.0:
    return "⚠️ Recuperação"  # Permitido uma segunda chance
else:
    return "❌ Reprovado"     # Abaixo do mínimo
```

**Threshold Padrão:** 7.0 (configurável na sidebar)

### 3. **Módulo de Visualização**

#### 3.1 Dashboard KPI
```python
# 4 métricas principais
1. Média Ponderada (com cor dinâmica)
2. Status (com emoji)
3. Progresso (% de conclusão)
4. Atividades Avaliadas (contador)
```

#### 3.2 Gráficos Plotly
- **Histograma**: Distribuição de notas
- **Gráfico de Barras Sobrepostos**: Pontos conquistados vs possíveis
- **Gráfico de Barras Horizontal**: Performance por atividade
- **Gráfico de Pizza**: Status das atividades

#### 3.3 Tabela de Dados
```python
# Exibição com:
├─ Filtro por texto
├─ Filtro por status (pendentes)
├─ Colunas formatadas (Nota: X.X/10)
└─ Coluna de contribuição percentual
```

### 4. **Módulo de Simulação**

```python
st.data_editor(df, use_container_width=True)
```

**Fluxo de Simulação:**
```
1. Usuário edita valor na coluna "Nota"
2. DataFrame é alterado em st.session_state
3. Recalcular average com novos valores
4. Exibir métrica delta (diferença)
5. Salvar em st.session_state.edited_data
```

**Recursos:**
- Validação em tempo real (0-10)
- Comparação com original (delta)
- Colunas desabilitadas (Status, Pontos)
- Salva simulação em session state

## 🔄 Fluxo de Dados

### Carregamento Inicial

```
[HTML Upload] 
    ↓
[Parse HTML] → DataFrame 1.0
    ↓
[Session State] 
    ↓
[Display Dashboard]
```

### Simulação

```
[Original DF]
    ↓
[st.data_editor]
    ↓
[Novo DF]
    ↓
[Recalcular Average]
    ↓
[Display Delta]
    ↓
[Save to Session State]
```

### Ciclo de Atualização Streamlit

```
1. User Action (Click, Input, etc)
   ↓
2. Execute app.py from top
   ↓
3. st.session_state preservado
   ↓
4. Widgets atualizam com novos valores
   ↓
5. Rerender página
```

## 📊 Estrutura do DataFrame

```python
pd.DataFrame({
    "Atividade": ["Business Question 1", "Gitflow Workflow", ...],
    "Status": ["Feito", "Feito", ...],
    "Pontos": [2.0, 4.0, ...],
    "Nota": [5.0, 8.5, None, ...],  # None para pendentes
    "Pendente": [False, False, True, ...]
})
```

**Dimensões Esperadas:**
- Linhas: ~15-20 atividades
- Colunas: 5 campos
- Tamanho: <100 KB em memória

## 🎨 Padrões de Design

### 1. **Caching com @st.cache_data**
```python
@st.cache_data
def parse_html_activities(html_path: str) -> pd.DataFrame
```
- **Por quê?** Evita re-parsing HTML a cada run
- **Sincronização?** Automática com hash do arquivo

### 2. **Session State para Estado Persistente**
```python
st.session_state.df_activities
st.session_state.edited_data
```
- **Por quê?** Dados persistem entre interações
- **Ciclo de vida?** Por sessão do navegador

### 3. **Widgets Interativos**
```python
st.slider()      # Threshold ajustável
st.file_uploader # Upload do HTML
st.data_editor   # Edição in-place
```

## ⚙️ Algoritmos Principais

### Cálculo de Média Ponderada (O(n))

```python
# Pseudocódigo
function calcular_media(df):
    notas_validas = filtrar(df.Nota != NaN)
    
    if notas_validas.vazio():
        retornar 0.0
    
    soma_ponderada = 0
    soma_pesos = 0
    
    for cada linha em notas_validas:
        soma_ponderada += linha.Nota × linha.Pontos
        soma_pesos += linha.Pontos
    
    media = soma_ponderada / soma_pesos
    retornar media
```

### Validação de Dados (O(n))

```python
# Pseudocódigo
function validar_nota(valor):
    if tipo(valor) != float:
        retornar False
    
    if valor < 0 or valor > 10:
        retornar False
    
    retornar True
```

## 📈 Complexidade Computacional

| Operação | Complexidade | Tempo (18 atividades) |
|----------|--------------|----------------------|
| Parse HTML | O(n) | ~50ms |
| Calc Média | O(n) | <1ms |
| Render Dashboard | O(n) | ~100ms |
| Plotly Gráficos | O(n log n) | ~200ms |
| Data Editor | O(n) | ~150ms |
| **Total** | **O(n log n)** | **~500ms** |

## 🔐 Segurança

### Validações Implementadas
1. ✅ Verificação de tipo (float para Nota/Pontos)
2. ✅ Range check (0-10 para notas)
3. ✅ Tratamento de exceções em parsing
4. ✅ Sem execução de código arbitrário (BeautifulSoup)

### Dados Sensíveis
- ❌ Não armazenados em servidor
- ❌ Não salvos em cookies
- ✅ Apenas em memória (RAM) durante sessão
- ✅ Removidos ao fechar navegador

## 🧪 Testes Unitários (Exemplo)

```python
# test_app.py
import pytest
import pandas as pd
from app import calculate_weighted_average, get_approval_status

def test_calculate_weighted_average():
    df = pd.DataFrame({
        "Nota": [5.0, 10.0],
        "Pontos": [2, 2]
    })
    media, eval, total = calculate_weighted_average(df)
    assert media == 7.5
    assert eval == 4.0

def test_approval_status_approved():
    assert get_approval_status(8.0, 7.0) == "✅ Aprovado"

def test_approval_status_recovery():
    assert get_approval_status(6.0, 7.0) == "⚠️ Recuperação"
```

## 📚 Dependências e Versões

| Biblioteca | Versão | Uso |
|------------|--------|-----|
| streamlit | 1.28.1 | Framework Web |
| pandas | 2.1.3 | Processamento Dados |
| numpy | 1.24.3 | Cálculos Numéricos |
| beautifulsoup4 | 4.12.2 | Parsing HTML |
| plotly | 5.17.0 | Gráficos Interativos |
| requests | 2.31.0 | HTTP (opcional) |

## 🚀 Performance e Otimizações

### 1. Caching
```python
@st.cache_data
def parse_html_activities(...)
# Evita re-parsing do mesmo arquivo
```

### 2. Lazy Loading
```python
if "df_activities" not in st.session_state:
    st.session_state.df_activities = None
# Só processa se necessário
```

### 3. Renderização Eficiente
```python
st.plotly_chart(fig, use_container_width=True)
# Uso de container nativo para melhor performance
```

## 🔍 Debugging e Logging

### Modo Debug (Adicione ao app.py)
```python
import logging

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

logger.debug(f"DataFrame shape: {df.shape}")
logger.info(f"Média calculada: {media:.2f}")
```

### Inspecionar Session State
```python
if st.checkbox("🔧 Debug"):
    st.write("Session State:")
    st.write(st.session_state)
```

## 📖 Referências de Implementação

### Streamlit
- Widgets: https://docs.streamlit.io/library/api-reference
- Cache: https://docs.streamlit.io/library/get-started/caching
- Sessions: https://docs.streamlit.io/library/api-reference/session-state

### Pandas
- DataFrame: https://pandas.pydata.org/docs/reference/frame.html
- Filtering: https://pandas.pydata.org/docs/user_guide/indexing.html

### BeautifulSoup
- Parsing: https://www.crummy.com/software/BeautifulSoup/bs4/doc/

## 🎯 Próximas Evoluções

1. **Database**: Salvar histórico em SQLite
2. **Auth**: Login de alunos
3. **Export**: PDF e Excel
4. **Mobile**: App nativo
5. **ML**: Previsão de desempenho
6. **Social**: Comparação anônima

---

**Documento Técnico Versão 1.0**
Última atualização: 2024
