# 📚 AdaLove - Gestor de Notas Acadêmicas

**Plataforma web para gestão, simulação e análise de desempenho acadêmico do portal AdaLove (Inteli)**

## 📋 Descrição

Aplicação desenvolvida em **Streamlit** que permite aos alunos do Inteli:

- ✅ **Importar dados** do portal AdaLove (arquivo HTML)
- 📊 **Visualizar métricas** de desempenho em tempo real
- ✏️ **Simular notas** futuras para diferentes cenários
- 📈 **Analisar gráficos** interativos de performance
- 💾 **Acompanhar evolução** das atividades acadêmicas


## 💻 Como Usar
1. Acesse o portal **AdaLove** (https://adalove.inteli.edu.br)
2. Navegue até a página **"academic-life"** (Notas)
3. Faça download da página (Ctrl+S) como **HTML**
4. Na sidebar da aplicação, faça upload do arquivo HTML
5. O sistema processará automaticamente seus dados

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