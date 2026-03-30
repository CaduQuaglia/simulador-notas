# 📚 AdaLove - Gestor de Notas Acadêmicas

**Plataforma web para gestão, simulação e análise de desempenho acadêmico do portal AdaLove (Inteli)**

## 📋 Descrição

Aplicação desenvolvida em **Streamlit** que permite aos alunos do Inteli:

- ✅ **Importar dados** do portal AdaLove (arquivo HTML)
- 📊 **Visualizar métricas** de desempenho em tempo real
- ✏️ **Simular notas** futuras para diferentes cenários
- 📈 **Analisar gráficos** interativos de performance
- 💾 **Acompanhar evolução** das atividades acadêmicas

## 🚀 Funcionalidades Principais

### 1. **Dashboard de Desempenho (KPI)**
- Média ponderada calculada automaticamente
- Status de aprovação (Aprovado/Recuperação/Reprovado)
- Indicador de progresso em relação ao total de pontos
- Contador de atividades avaliadas e pendentes

### 2. **Visualizações Interativas**
- **Gráficos de Distribuição**: Frequência de notas com indicador de média
- **Gráficos de Barras**: Pontos conquistados vs. possíveis por atividade
- **Gráfico de Performance**: Notas por atividade em escala de cores
- **Gráfico de Pizza**: Resumo de status (avaliadas/pendentes)

### 3. **Simulador de Notas**
- Editor de dados integrado (data_editor do Streamlit)
- Edição em tempo real com recálculo automático
- Comparação entre cenários (original vs. simulado)
- Visualização de delta de mudanças

### 4. **Tabela Detalhada**
- Busca por termo em atividades
- Filtro para mostrar apenas pendentes
- Visualização formatada com emojis
- Coluna de contribuição percentual

### 5. **Análise Estatística**
- Estatísticas descritivas (máx, mín, média, desvio padrão)
- Recomendações inteligentes baseadas no desempenho
- Insight sobre próximos passos
- Lista de atividades pendentes

## 📦 Dependências

```
streamlit==1.28.1
pandas==2.1.3
numpy==1.24.3
beautifulsoup4==4.12.2
plotly==5.17.0
requests==2.31.0
```

## 💻 Instalação

### Passo 1: Clonar ou baixar os arquivos
```bash
# Se tiver git
git clone <repo-url>
cd adalove-notas

# Ou faça download manual dos arquivos
```

### Passo 2: Criar ambiente virtual (recomendado)
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

### Passo 3: Instalar dependências
```bash
pip install -r requirements.txt
```

## 🎯 Como Usar

### Opção 1: Executar a aplicação
```bash
streamlit run app.py
```

A aplicação abrirá em `http://localhost:8501`

### Opção 2: Usar com dados de exemplo
1. Abra a aplicação
2. Na sidebar, marque **"🎯 Usar dados de exemplo"**
3. Explore o dashboard com dados pré-carregados

### Opção 3: Usar com seus dados
1. Acesse o portal **AdaLove** (https://adalove.inteli.edu.br)
2. Navegue até a página **"academic-life"** (Notas)
3. Faça download da página como **HTML** (Ctrl+S)
4. Na sidebar da aplicação, faça upload do arquivo HTML
5. O sistema processará automaticamente seus dados

## 🏗️ Arquitetura e Estrutura do Código

```
app.py
├── CONFIGURAÇÃO STREAMLIT
│   └── set_page_config, CSS customizado
├── FUNÇÕES DE PARSING HTML
│   └── parse_html_activities()
├── FUNÇÕES DE CÁLCULO
│   ├── calculate_weighted_average()
│   ├── get_approval_status()
│   └── get_status_color()
├── INICIALIZAÇÃO SESSION STATE
│   └── Variáveis de sessão
└── FUNÇÃO MAIN
    ├── Sidebar (configurações)
    ├── Dashboard KPI
    ├── Visualizações (gráficos)
    ├── Simulador
    ├── Tabela Detalhada
    ├── Análise
    └── Rodapé
```

## 🔧 Configurações

Na **sidebar**, você pode:

1. **Upload do HTML**: Selecionar arquivo da página de notas
2. **Nota Mínima para Aprovação**: Ajustar o threshold (padrão: 7.0)
3. **Informações Gerais**: Ver resumo de atividades

## 📊 Estrutura de Dados (DataFrame)

O DataFrame carregado contém as seguintes colunas:

| Coluna | Tipo | Descrição |
|--------|------|-----------|
| `Atividade` | string | Nome da atividade/tarefa |
| `Status` | string | Status atual (Feito/Não feito) |
| `Pontos` | float | Peso/valor total da atividade |
| `Nota` | float | Nota obtida pelo aluno (0-10) ou NaN |
| `Pendente` | bool | Indica se aguarda avaliação |

## 🧮 Cálculos e Lógica

### Média Ponderada
```
Média = Σ(Nota × Peso) / Σ(Peso)

Apenas atividades com notas são consideradas.
Atividades pendentes (nota = "-") são ignoradas.
```

### Status de Aprovação
- **Aprovado**: Média ≥ Threshold (padrão 7.0) ✅
- **Recuperação**: 5.0 ≤ Média < 7.0 ⚠️
- **Reprovado**: Média < 5.0 ❌

### Contribuição Percentual
```
Contribuição = (Nota × Peso) / 10
```

## 🎨 Customizações

### Alterar cores do tema
No arquivo `app.py`, na seção CSS, modifique os valores de `background`:

```css
.metric-card {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    /* Altere os códigos HEX para suas cores preferidas */
}
```

### Alterar threshold de aprovação
```python
# Padrão é 7.0, mas pode ser ajustado na sidebar
threshold = st.slider("...", 0.0, 10.0, 7.0, 0.1)
```

### Adicionar mais métricas
Adicione novas colunas no DataFrame após parsing:

```python
# Exemplo: Adicionar coluna de categoria de atividade
df["Categoria"] = df["Atividade"].apply(categorizar_atividade)
```

## 🐛 Troubleshooting

### Erro: "ModuleNotFoundError: No module named 'streamlit'"
```bash
# Solução: Instalar dependências
pip install -r requirements.txt
```

### Erro: "HTMLParserError"
- Verifique se o arquivo HTML foi salvo corretamente do AdaLove
- Tente re-fazer download da página

### A tabela não carrega
- Verifique se o HTML contém as tags `<tr class="styled-tr">`
- O arquivo HTML pode estar incompleto

### Simulação não recalcula
- Limpe o cache do navegador (Ctrl+Shift+Delete)
- Ou use `st.cache_clear()` no código

## 📚 Recursos Adicionais

- **Documentação Streamlit**: https://docs.streamlit.io
- **BeautifulSoup4**: https://www.crummy.com/software/BeautifulSoup/
- **Plotly**: https://plotly.com/python/
- **Pandas**: https://pandas.pydata.org/docs/

## 🔐 Privacidade e Segurança

- ⚠️ Não armazene dados sensíveis
- 📁 Arquivos carregados são processados localmente
- 🗑️ Dados são removidos ao fechar a sessão
- ✅ Sem conexão com servidores externos

## 📝 Licença

Este projeto é fornecido como está para fins educacionais.

## 👨‍💻 Autor

**Desenvolvido por**: Desenvolvedor Python Sênior
**Especialização**: Streamlit, Ciência de Dados, Web Scraping
**Data**: 2024

## 📞 Suporte

Para dúvidas ou problemas:
1. Verifique a seção Troubleshooting
2. Consulte a documentação oficial das bibliotecas
3. Abra uma issue no repositório

---

**Desenvolvido com ❤️ para Inteli - Instituto de Tecnologia e Liderança**
