"""
EXEMPLOS AVANÇADOS - AdaLove Gestor de Notas

Este arquivo contém exemplos de como estender e customizar a aplicação.
"""

# ==============================================================================
# EXEMPLO 1: Análise Comparativa Entre Períodos
# ==============================================================================

def exemplo_comparacao_periodos():
    """
    Compara desempenho entre diferentes períodos acadêmicos.
    """
    import streamlit as st
    import pandas as pd
    import plotly.graph_objects as go
    
    # Simulando dados de dois períodos
    periodo1 = pd.DataFrame({
        "Atividade": ["A1", "A2", "A3"],
        "Nota": [5.0, 6.0, 7.0],
        "Pontos": [2, 3, 4]
    })
    
    periodo2 = pd.DataFrame({
        "Atividade": ["A1", "A2", "A3"],
        "Nota": [7.0, 8.0, 8.5],
        "Pontos": [2, 3, 4]
    })
    
    # Calcular médias
    def calc_media(df):
        return (df["Nota"] * df["Pontos"]).sum() / df["Pontos"].sum()
    
    # Criar gráfico comparativo
    fig = go.Figure(data=[
        go.Bar(name='Período 1', x=periodo1["Atividade"], y=periodo1["Nota"]),
        go.Bar(name='Período 2', x=periodo2["Atividade"], y=periodo2["Nota"])
    ])
    
    st.plotly_chart(fig)


# ==============================================================================
# EXEMPLO 2: Exportar Relatório em PDF
# ==============================================================================

def exemplo_relatorio_pdf():
    """
    Gera um relatório completo em PDF com dados e gráficos.
    """
    from reportlab.lib.pagesizes import letter
    from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph
    from reportlab.lib.styles import getSampleStyleSheet
    import pandas as pd
    
    def gerar_relatorio(df, filename="relatorio_notas.pdf"):
        """Gera relatório PDF com dados das atividades."""
        
        # Criar documento
        doc = SimpleDocTemplate(filename, pagesize=letter)
        elements = []
        
        # Título
        styles = getSampleStyleSheet()
        title = Paragraph("Relatório de Desempenho Acadêmico", styles['Title'])
        elements.append(title)
        
        # Tabela com dados
        data = [["Atividade", "Nota", "Pontos"]]
        for _, row in df.iterrows():
            data.append([
                row["Atividade"][:30],
                f"{row['Nota']:.1f}" if pd.notna(row['Nota']) else "-",
                f"{row['Pontos']:.0f}"
            ])
        
        table = Table(data)
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), '#667eea'),
            ('TEXTCOLOR', (0, 0), (-1, 0), 'white'),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 14),
        ]))
        
        elements.append(table)
        
        # Salvar
        doc.build(elements)
        return filename


# ==============================================================================
# EXEMPLO 3: Integração com Banco de Dados
# ==============================================================================

def exemplo_banco_dados():
    """
    Armazena e recupera dados de desempenho em SQL.
    """
    import sqlite3
    import pandas as pd
    
    def criar_banco():
        """Cria tabela de notas em SQLite."""
        conn = sqlite3.connect("notas.db")
        cursor = conn.cursor()
        
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS atividades (
                id INTEGER PRIMARY KEY,
                nome TEXT NOT NULL,
                nota REAL,
                pontos REAL,
                data_criacao DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        conn.commit()
        conn.close()
    
    def salvar_notas(df):
        """Salva DataFrame no banco."""
        conn = sqlite3.connect("notas.db")
        df.to_sql("atividades", conn, if_exists="append", index=False)
        conn.close()
    
    def carregar_notas():
        """Carrega dados do banco."""
        conn = sqlite3.connect("notas.db")
        df = pd.read_sql_query("SELECT * FROM atividades", conn)
        conn.close()
        return df


# ==============================================================================
# EXEMPLO 4: Machine Learning - Previsão de Notas
# ==============================================================================

def exemplo_ml_previsao():
    """
    Usa ML para prever nota em atividades futuras.
    """
    from sklearn.linear_model import LinearRegression
    import numpy as np
    import pandas as pd
    
    def prever_proximas_notas(df):
        """
        Treina modelo para prever notas futuras.
        Usa ordem da atividade como feature.
        """
        # Preparar dados
        df_avaliadas = df[~df["Nota"].isna()].reset_index(drop=True)
        
        X = np.array(range(len(df_avaliadas))).reshape(-1, 1)
        y = df_avaliadas["Nota"].values
        
        # Treinar modelo
        model = LinearRegression()
        model.fit(X, y)
        
        # Prever próximas 5 atividades
        proximas = np.array(range(len(df_avaliadas), len(df_avaliadas) + 5)).reshape(-1, 1)
        predicoes = model.predict(proximas)
        
        return predicoes
    
    # Exemplo de uso
    # df = st.session_state.df_activities
    # previsoes = prever_proximas_notas(df)
    # st.write("Notas previstas para próximas atividades:", previsoes)


# ==============================================================================
# EXEMPLO 5: Notificações e Alertas
# ==============================================================================

def exemplo_notificacoes():
    """
    Sistema de alertas e notificações inteligentes.
    """
    import streamlit as st
    
    def verificar_alertas(df, threshold=7.0):
        """Gera alertas baseado nos dados."""
        alertas = []
        
        # Alerta 1: Média baixa
        media = (df["Nota"] * df["Pontos"]).sum() / df["Pontos"].sum()
        if media < threshold:
            alertas.append({
                "tipo": "warning",
                "mensagem": f"⚠️ Sua média ({media:.2f}) está abaixo do limite ({threshold})!"
            })
        
        # Alerta 2: Atividades pendentes
        pendentes = df[df["Pendente"]]
        if len(pendentes) > 0:
            alertas.append({
                "tipo": "info",
                "mensagem": f"ℹ️ Você tem {len(pendentes)} atividades aguardando avaliação."
            })
        
        # Alerta 3: Nota muito baixa
        df_avaliadas = df[~df["Nota"].isna()]
        if len(df_avaliadas) > 0 and df_avaliadas["Nota"].min() < 4.0:
            alertas.append({
                "tipo": "error",
                "mensagem": f"❌ Atividade com nota muito baixa detectada ({df_avaliadas['Nota'].min():.1f})!"
            })
        
        return alertas
    
    # Exemplo de uso
    # alertas = verificar_alertas(df)
    # for alerta in alertas:
    #     if alerta["tipo"] == "warning":
    #         st.warning(alerta["mensagem"])
    #     elif alerta["tipo"] == "info":
    #         st.info(alerta["mensagem"])


# ==============================================================================
# EXEMPLO 6: Ranking e Comparação Entre Alunos
# ==============================================================================

def exemplo_ranking():
    """
    Cria ranking anônimo de desempenho entre alunos.
    (Use com cuidado respeitando privacidade!)
    """
    import pandas as pd
    
    # Simulando dados de múltiplos alunos
    alunos_dados = {
        "Aluno_A": pd.DataFrame({
            "Nota": [5.0, 8.5, 6.0, 6.4],
            "Pontos": [2, 4, 3, 2]
        }),
        "Aluno_B": pd.DataFrame({
            "Nota": [7.0, 7.0, 7.0, 8.0],
            "Pontos": [2, 4, 3, 2]
        }),
        "Aluno_C": pd.DataFrame({
            "Nota": [4.0, 5.0, 5.0, 4.5],
            "Pontos": [2, 4, 3, 2]
        })
    }
    
    def calcular_medias(dados_alunos):
        """Calcula médias de todos alunos."""
        medias = {}
        for aluno, df in dados_alunos.items():
            media = (df["Nota"] * df["Pontos"]).sum() / df["Pontos"].sum()
            medias[aluno] = media
        
        # Ordenar por média
        ranking = sorted(medias.items(), key=lambda x: x[1], reverse=True)
        return ranking
    
    ranking = calcular_medias(alunos_dados)
    print("Ranking (Anônimo):")
    for posicao, (aluno, media) in enumerate(ranking, 1):
        print(f"{posicao}º lugar: {media:.2f}")


# ==============================================================================
# EXEMPLO 7: Integração com Google Sheets
# ==============================================================================

def exemplo_google_sheets():
    """
    Sincroniza dados com Google Sheets para backup.
    """
    # Requer bibliotecas: pip install gspread oauth2client
    
    def salvar_em_google_sheets(df, spreadsheet_name):
        """
        Salva DataFrame em Google Sheet.
        Requer autenticação OAuth2.
        """
        try:
            import gspread
            from oauth2client.service_account import ServiceAccountCredentials
            
            scope = ['https://spreadsheets.google.com/feeds']
            creds = ServiceAccountCredentials.from_json_keyfile_name(
                'credentials.json', scope
            )
            client = gspread.authorize(creds)
            
            sheet = client.open(spreadsheet_name).sheet1
            
            # Limpar e preencer
            sheet.clear()
            
            # Adicionar cabeçalho
            sheet.append_row(df.columns.tolist())
            
            # Adicionar dados
            for _, row in df.iterrows():
                sheet.append_row(row.tolist())
            
            print(f"✅ Dados salvos em '{spreadsheet_name}'")
            
        except ImportError:
            print("⚠️ Instale: pip install gspread oauth2client")
        except Exception as e:
            print(f"❌ Erro: {e}")


# ==============================================================================
# EXEMPLO 8: Dashboard Customizado
# ==============================================================================

def exemplo_dashboard_customizado():
    """
    Cria dashboard com múltiplas abas customizadas.
    """
    import streamlit as st
    import pandas as pd
    import plotly.graph_objects as go
    
    # Criar abas
    tabs = st.tabs([
        "📊 Overview",
        "📈 Análise Detalhada",
        "🎯 Metas",
        "📚 Recursos"
    ])
    
    with tabs[0]:
        # Overview rápido
        st.metric("Média", "6.8")
        st.metric("Status", "Recuperação ⚠️")
    
    with tabs[1]:
        # Análise mais profunda
        st.subheader("Análise de Tendências")
        # Adicionar gráficos
    
    with tabs[2]:
        # Metas pessoais
        st.write("Defina suas metas de desempenho...")
        meta_media = st.slider("Meta de média", 5.0, 10.0, 7.0)
    
    with tabs[3]:
        # Links úteis
        st.markdown("""
        - 📖 [Documentação Streamlit](https://docs.streamlit.io)
        - 📊 [Plotly](https://plotly.com)
        - 🐼 [Pandas](https://pandas.pydata.org)
        """)


# ==============================================================================
# EXEMPLO 9: Validação e Limpeza de Dados
# ==============================================================================

def exemplo_validacao_dados():
    """
    Funções para validar e limpar dados de entrada.
    """
    import pandas as pd
    import numpy as np
    
    def validar_dados(df):
        """Valida integridade dos dados."""
        problemas = []
        
        # Verificar colunas obrigatórias
        colunas_obrigatorias = ["Atividade", "Nota", "Pontos"]
        for col in colunas_obrigatorias:
            if col not in df.columns:
                problemas.append(f"❌ Coluna obrigatória faltando: {col}")
        
        # Verificar valores de nota (0-10)
        df_notas = df[~df["Nota"].isna()]
        invalidas = df_notas[(df_notas["Nota"] < 0) | (df_notas["Nota"] > 10)]
        if not invalidas.empty:
            problemas.append(f"⚠️ {len(invalidas)} notas fora do intervalo 0-10")
        
        # Verificar pontos positivos
        if (df["Pontos"] <= 0).any():
            problemas.append("❌ Encontrados pontos com valor <= 0")
        
        # Verificar duplicatas
        if df.duplicated(subset=["Atividade"]).any():
            problemas.append("⚠️ Atividades duplicadas detectadas")
        
        return problemas
    
    def limpar_dados(df):
        """Remove inconsistências."""
        df_limpo = df.copy()
        
        # Remover espaços em branco
        df_limpo["Atividade"] = df_limpo["Atividade"].str.strip()
        
        # Converter tipos
        df_limpo["Nota"] = pd.to_numeric(df_limpo["Nota"], errors='coerce')
        df_limpo["Pontos"] = pd.to_numeric(df_limpo["Pontos"], errors='coerce')
        
        # Remover duplicatas
        df_limpo = df_limpo.drop_duplicates(subset=["Atividade"])
        
        # Limitar notas ao intervalo [0, 10]
        df_limpo.loc[df_limpo["Nota"] > 10, "Nota"] = 10
        df_limpo.loc[df_limpo["Nota"] < 0, "Nota"] = 0
        
        return df_limpo


# ==============================================================================
# EXEMPLO 10: Cache e Performance
# ==============================================================================

def exemplo_performance():
    """
    Otimizações para melhorar performance.
    """
    import streamlit as st
    import pandas as pd
    
    @st.cache_data
    def carregar_dados_grande(arquivo):
        """Cache evita recarregar dados a cada interação."""
        return pd.read_csv(arquivo)
    
    @st.cache_resource
    def criar_conexao_db():
        """Cache para conexão com banco."""
        import sqlite3
        return sqlite3.connect("notas.db")
    
    # Usar cache
    # df = carregar_dados_grande("dados.csv")
    # conn = criar_conexao_db()


# ==============================================================================
# EXECUTAR EXEMPLOS
# ==============================================================================

if __name__ == "__main__":
    print("=" * 60)
    print("EXEMPLOS AVANÇADOS - AdaLove Gestor de Notas")
    print("=" * 60)
    print()
    print("Para usar estes exemplos, copie a função desejada e")
    print("integre ao app.py principal conforme sua necessidade.")
    print()
    print("Exemplos disponíveis:")
    print("1. Análise Comparativa Entre Períodos")
    print("2. Exportar Relatório em PDF")
    print("3. Integração com Banco de Dados")
    print("4. Machine Learning - Previsão de Notas")
    print("5. Notificações e Alertas")
    print("6. Ranking e Comparação Entre Alunos")
    print("7. Integração com Google Sheets")
    print("8. Dashboard Customizado")
    print("9. Validação e Limpeza de Dados")
    print("10. Cache e Performance")
    print()
    print("=" * 60)
