# 🚀 Guia Rápido - AdaLove Gestor de Notas

## ⏱️ 30 Segundos para Começar

### 1️⃣ Instalação
```bash
pip install -r requirements.txt
```

### 2️⃣ Executar
```bash
streamlit run app.py
```

### 3️⃣ Usar
- Abra `http://localhost:8501`
- Clique em **"🎯 Usar dados de exemplo"** ou upload seu HTML do AdaLove
- Explore os dashboards!

---

## 📖 Guia Completo

### Interface Principal

```
┌─────────────────────────────────────────────────┐
│  📚 AdaLove - Gestor de Notas Acadêmicas       │
│  Plataforma de Gestão e Simulação de Notas     │
└─────────────────────────────────────────────────┘

┌─── SIDEBAR ─────────────────┐  ┌─── MAIN ──────────────────┐
│ ⚙️ Configurações            │  │ 📊 Dashboard KPI          │
│ 📄 Upload HTML              │  │ • Média Ponderada         │
│ 📊 Threshold: [———7.0———]   │  │ • Status                  │
│ 📈 Informações Gerais       │  │ • Progresso               │
│ • Total: 18 atividades      │  │ • Atividades Avaliadas    │
│ • Avaliadas: 18             │  │                           │
│ • Pendentes: 0              │  │ 📈 Tabs:                  │
│ • Pontos: 48.0              │  │ 1. Gráficos               │
└─────────────────────────────┘  │ 2. Editor de Simulação    │
                                  │ 3. Tabela Detalhada       │
                                  │                           │
                                  │ 📊 Análise Detalhada      │
                                  └───────────────────────────┘
```

### Seções Principais

#### 🎯 Dashboard KPI (Início)
- **Métrica Principal**: Média Ponderada (0-10)
- **Status**: Aprovado/Recuperação/Reprovado
- **Progresso**: Percentual de conclusão
- **Atividades**: Contagem de avaliadas/pendentes

#### 📈 Aba de Gráficos
1. **Distribuição de Notas**: Frequência com média destacada
2. **Pontos por Atividade**: Conquistados vs. possíveis
3. **Performance**: Notas em ordem ascendente
4. **Status**: Pizza de avaliadas vs. pendentes

#### ✏️ Aba de Simulação
- Editor interativo de notas
- Recálculo automático da média
- Comparação com original
- Botão para salvar simulação

#### 📋 Aba Tabela Detalhada
- Busca por termo
- Filtro de pendentes
- Visão formatada com emojis
- Coluna de contribuição

#### 📊 Análise Detalhada
- Estatísticas descritivas
- Recomendações inteligentes
- Lista de atividades pendentes

---

## 🔑 Funcionalidades-Chave

### 1. Upload do HTML
```
Sidebar → 📄 Upload do HTML → Selecionar arquivo
         (salvo do AdaLove)
         ↓
    [Processado Automaticamente]
    ↓
    Dashboard atualizado com seus dados
```

### 2. Dados de Exemplo
```
Sidebar → 🎯 Usar dados de exemplo
         ↓
    Carrega 18 atividades pré-configuradas
    ↓
    Explore livremente sem seus dados pessoais
```

### 3. Ajustar Threshold
```
Sidebar → Nota Mínima para Aprovação [——●——→] 7.0
         ↓
    Mude o slider (0-10)
    ↓
    KPI e status se atualizam em tempo real
```

### 4. Simular Notas
```
Tab: ✏️ Editor de Simulação
    ↓
Edite valores na coluna "Nota"
    ↓
Veja a média recalcular instantaneamente
    ↓
Compare com a simulação original
```

---

## 💡 Dicas e Truques

### Dica 1: Explorar Cenários
Teste diferentes notas no simulador:
- "E se eu tirar 8.5 na próxima?"
- "Qual nota preciso para aprovar?"
- "Como fico com 8.0 de média?"

### Dica 2: Interpretar Gráficos
- 🟢 **Verde intenso**: Notas altas
- 🟡 **Amarelo**: Notas médias
- 🔴 **Vermelho**: Notas baixas

### Dica 3: Usar a Busca
Procure por termo específico:
```
Buscar: "GRADED"
        ↓
    Mostra apenas atividades com "[GRADED ACTIVITY]"
```

### Dica 4: Filtrar Pendentes
```
☑️ Mostrar apenas pendentes
   ↓
   Lista apenas atividades aguardando nota
   ↓
   Ajuda a priorizar o que falta
```

---

## 📊 Exemplo de Análise

### Scenario: Aluno com Média 6.5

```
📊 Dashboard mostra:
├─ Média Ponderada: 6.5/10
├─ Status: ⚠️ Recuperação
├─ Progresso: 100% (todas avaliadas)
└─ Atividades: 18/18

📈 Gráfico de Distribuição:
├─ Notas distribuídas entre 5.0 e 9.0
├─ Maioria entre 5.0 e 6.8
├─ Média destacada em 6.5
└─ Precisa focar em atividades com notas baixas

✏️ Simulador sugere:
├─ Se melhorar 3 atividades de 5.5 para 7.0
├─ Média sobe para ~7.1
├─ Passa para Aprovado ✅
└─ Aproveita oportunidades de recuperação
```

---

## 🔧 Troubleshooting Rápido

### ❌ "Arquivo não processado"
```
✅ Solução:
1. Certifique-se que é HTML (não PDF)
2. Salve como página completa do AdaLove
3. Tente novamente
```

### ❌ "Tabela vazia"
```
✅ Solução:
1. Use "Dados de exemplo" primeiro
2. Verifique se o HTML tem as tabelas visíveis
3. Limpe cache (Ctrl+Shift+Del)
```

### ❌ "Simulação não recalcula"
```
✅ Solução:
1. Recarregue a página (F5)
2. Clique em outra aba e volte
3. Abra em navegador privado
```

---

## 📚 Estrutura de Dados Esperada

Seu HTML deve conter uma tabela com estrutura como:

```html
<tr class="styled-tr">
    <td>Nome da Atividade</td>
    <td>...</td>
    <td>Status</td>
    <td>Pontos</td>
    <td>Nota (ou "-")</td>
    <td>Feedback</td>
</tr>
```

---

## 🎨 Customizações Comuns

### Mudar cor do tema
No `app.py`, procure por:
```python
style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);"
```
Altere os códigos HEX.

### Adicionar mais atividades
No arquivo `generate_example_data.py`:
```python
"Atividade": [
    "Atividade Existente",
    "Nova Atividade",  # ← Adicione aqui
]
```

### Mudar status padrão
No `app.py`, procure por:
```python
threshold = st.slider(..., 7.0, ...)  # ← Mude de 7.0
```

---

## 📱 Responsividade

A aplicação funciona bem em:
- ✅ Desktop (recomendado)
- ✅ Tablet (navegação lateral)
- ⚠️ Mobile (layout comprimido)

### Para mobile melhor:
Use o menu "☰" para esconder a sidebar

---

## 🔐 Segurança & Privacidade

- ✅ Dados processados localmente
- ✅ Sem envio para servidores externos
- ✅ Removidos ao fechar browser
- ✅ Compatível com dados pessoais

**Nunca compartilhe seu arquivo HTML com terceiros!**

---

## 📞 Perguntas Frequentes

**P: Posso usar no meu celular?**
R: Sim, mas desktop é melhor para ver gráficos.

**P: Os dados são salvos?**
R: Não, recarregue a página = perde dados. Use "💾 Salvar Simulação".

**P: Posso editar a tabela?**
R: Apenas no simulador (tab 2). A tab 3 é apenas visualização.

**P: Como exporto os gráficos?**
R: Clique na câmera 📷 (canto direito de cada gráfico Plotly).

---

## 🌟 Recursos Avançados

### Acessar dados programaticamente
Se souber Python, edite `app.py`:

```python
# Após carregar dados
df = st.session_state.df_activities

# Análise customizada
top_3 = df.nlargest(3, "Nota")
st.dataframe(top_3)
```

### Exportar dados
Adicione ao final do código:

```python
csv = df.to_csv(index=False)
st.download_button(
    "📥 Baixar CSV",
    csv,
    "notas.csv"
)
```

---

## 📖 Referências

- **Streamlit Docs**: https://docs.streamlit.io
- **Plotly**: https://plotly.com/python
- **Pandas**: https://pandas.pydata.org

---

**Desenvolvido com ❤️ para Inteli**

Última atualização: 2024
