"""
Aplicação Streamlit para Gestão e Simulação de Notas Acadêmicas - AdaLove (Inteli)
Desenvolvido por: Desenvolvedor Python Sênior - Especialista em Streamlit & Data Science
"""

import streamlit as st
import pandas as pd
import numpy as np
from bs4 import BeautifulSoup
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
import warnings

warnings.filterwarnings("ignore")

# ============================================================================
# CONFIGURAÇÃO STREAMLIT
# ============================================================================

st.set_page_config(
    page_title="AdaLove - Gestor de Notas",
    page_icon="📚",
    layout="wide",
    initial_sidebar_state="expanded"
)

# CSS Customizado
st.markdown("""
    <style>
        .metric-card {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            padding: 20px;
            border-radius: 10px;
            color: white;
            text-align: center;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        }
        .metric-value {
            font-size: 2.5em;
            font-weight: bold;
            margin: 10px 0;
        }
        .metric-label {
            font-size: 0.9em;
            opacity: 0.9;
        }
        .status-approved {
            color: #2ecc71;
            font-weight: bold;
        }
        .status-recovery {
            color: #f39c12;
            font-weight: bold;
        }
        .status-pending {
            color: #e74c3c;
            font-weight: bold;
        }
    </style>
""", unsafe_allow_html=True)

# ============================================================================
# FUNÇÕES DE PARSING HTML
# ============================================================================

@st.cache_data
def parse_html_activities(html_path: str) -> pd.DataFrame:
    """
    Extrai dados de atividades do HTML do portal AdaLove.
    
    Args:
        html_path: Caminho para o arquivo HTML
        
    Returns:
        DataFrame com as atividades extraídas
    """
    with open(html_path, "r", encoding="utf-8") as file:
        soup = BeautifulSoup(file, "html.parser")
    
    activities = []
    table_rows = soup.find_all("tr", class_="styled-tr")
    
    for row in table_rows:
        cells = row.find_all("td")
        
        if len(cells) >= 5:
            # Extrai dados de cada célula
            activity_name = cells[0].get_text(strip=True)
            status = cells[2].get_text(strip=True)
            points_str = cells[3].get_text(strip=True)
            grade_str = cells[4].get_text(strip=True)
            
            # Processa pontos (peso)
            try:
                points = float(points_str)
            except ValueError:
                points = 0.0
            
            # Processa notas (trata "-" como pendente)
            if grade_str.strip() == "-":
                grade = np.nan
                is_pending = True
            else:
                try:
                    grade = float(grade_str)
                    is_pending = False
                except ValueError:
                    grade = np.nan
                    is_pending = True
            
            activities.append({
                "Atividade": activity_name,
                "Status": status,
                "Pontos": points,
                "Nota": grade,
                "Pendente": is_pending
            })
    
    return pd.DataFrame(activities)

# ============================================================================
# FUNÇÕES DE CÁLCULO
# ============================================================================

def calculate_weighted_average(df: pd.DataFrame) -> tuple:
    """
    Calcula a média ponderada das notas.
    
    Args:
        df: DataFrame com as atividades
        
    Returns:
        Tupla (média, total_pontos_avaliados, total_pontos_possíveis)
    """
    # Filtra apenas atividades com notas (não pendentes)
    evaluated = df[~df["Nota"].isna()].copy()
    
    if evaluated.empty or evaluated["Pontos"].sum() == 0:
        return 0.0, 0.0, df["Pontos"].sum()
    
    # Cálculo da média ponderada
    weighted_sum = (evaluated["Nota"] * evaluated["Pontos"]).sum()
    total_points = evaluated["Pontos"].sum()
    
    weighted_avg = weighted_sum / total_points if total_points > 0 else 0.0
    
    return weighted_avg, total_points, df["Pontos"].sum()

def get_approval_status(average: float, threshold: float = 7.0) -> str:
    """
    Retorna o status de aprovação baseado na média.
    """
    if average >= threshold:
        return "✅ Aprovado"
    elif average >= 5.0:
        return "⚠️ Recuperação"
    else:
        return "❌ Reprovado"

def get_status_color(average: float, threshold: float = 7.0) -> str:
    """
    Retorna a cor do status.
    """
    if average >= threshold:
        return "#2ecc71"  # Verde
    elif average >= 5.0:
        return "#f39c12"   # Laranja
    else:
        return "#e74c3c"   # Vermelho

# ============================================================================
# INICIALIZAÇÃO DO SESSION STATE
# ============================================================================

if "df_activities" not in st.session_state:
    st.session_state.df_activities = None

if "edited_data" not in st.session_state:
    st.session_state.edited_data = None

# ============================================================================
# FUNÇÃO PRINCIPAL
# ============================================================================

def main():
    """Função principal da aplicação."""
    
    # Header
    col1, col2 = st.columns([0.8, 0.2])
    with col1:
        st.title("📚 AdaLove - Gestor de Notas Acadêmicas")
        st.markdown("**Plataforma de Gestão e Simulação de Desempenho Acadêmico**")
    with col2:
        st.write("")
        st.write("")
        st.metric("Data Atual", datetime.now().strftime("%d/%m/%Y"))
    
    st.divider()
    
    # Sidebar - Configurações
    with st.sidebar:
        st.header("⚙️ Configurações")
        
        uploaded_file = st.file_uploader(
            "📄 Upload do HTML AdaLove",
            type=["html"],
            help="Selecione o arquivo HTML da página de notas do portal AdaLove"
        )
        
        if uploaded_file:
            # Salva arquivo temporário
            import tempfile
            with tempfile.NamedTemporaryFile(delete=False, suffix=".html") as f:
                f.write(uploaded_file.getvalue())
                temp_path = f.name
            
            # Carrega dados
            try:
                st.session_state.df_activities = parse_html_activities(temp_path)
                st.success("✅ Arquivo processado com sucesso!")
            except Exception as e:
                st.error(f"❌ Erro ao processar o arquivo: {e}")
        
        st.divider()
        
        threshold = st.slider(
            "📊 Nota Mínima para Aprovação",
            0.0, 10.0, 7.0, 0.1,
            help="Define a nota mínima considerada como aprovado"
        )
        
        st.divider()
        
        st.markdown("### 📈 Informações Gerais")
        if st.session_state.df_activities is not None:
            df = st.session_state.df_activities
            st.metric("Total de Atividades", len(df))
            st.metric("Atividades Avaliadas", len(df[~df["Nota"].isna()]))
            st.metric("Atividades Pendentes", len(df[df["Pendente"]]))
            st.metric("Pontos Totais", f"{df['Pontos'].sum():.1f}")
    
    # Verificar se dados foram carregados
    if st.session_state.df_activities is None:
        st.info("👈 Por favor, carregue o arquivo HTML da página de notas do AdaLove para começar.")
        
        # Dados de exemplo para demonstração
        if st.checkbox("🎯 Usar dados de exemplo"):
            example_data = {
                "Atividade": [
                    "Business Question 1",
                    "[GRADED ACTIVITY] Gitflow Workflow",
                    "PROJECT AND BUSINESS UNDERSTANDING",
                    "FUNCTIONAL AND NON-FUNCTIONAL REQUIREMENTS",
                    "EVOLUTIONARY PROJECT MANAGEMENT",
                    "Differentiation and its applications",
                    "[GRADED ACTIVITY] Stakeholder Map",
                    "TECHNICAL SOLUTION (DESIGN)",
                    "DATA MODELING",
                    "SERVICE BLUEPRINT"
                ],
                "Status": ["Feito"] * 10,
                "Pontos": [2, 4, 3, 2, 3, 3, 3, 3, 3, 2],
                "Nota": [5.0, 8.5, 6.0, 6.4, 6.8, 8.5, 8.5, 5.4, 5.1, 5.1],
                "Pendente": [False] * 10
            }
            st.session_state.df_activities = pd.DataFrame(example_data)
        else:
            return
    
    # ========================================================================
    # SEÇÃO 1: DASHBOARD KPI
    # ========================================================================
    
    st.header("📊 Dashboard de Desempenho")
    
    df = st.session_state.df_activities.copy()
    average, total_evaluated, total_possible = calculate_weighted_average(df)
    status = get_approval_status(average, threshold)
    status_color = get_status_color(average, threshold)
    
    # Métricas principais
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown(f"""
            <div class="metric-card" style="background: linear-gradient(135deg, {status_color} 0%, {status_color}cc 100%);">
                <div class="metric-label">Média Ponderada</div>
                <div class="metric-value">{average:.2f}</div>
                <div class="metric-label">/ 10.0</div>
            </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
            <div class="metric-card" style="background: linear-gradient(135deg, #3498db 0%, #2980b9 100%);">
                <div class="metric-label">Status</div>
                <div class="metric-value" style="font-size: 1.8em;">{status}</div>
                <div class="metric-label">Limite: {threshold:.1f}</div>
            </div>
        """, unsafe_allow_html=True)
    
    with col3:
        percentage = (total_evaluated / total_possible * 100) if total_possible > 0 else 0
        st.markdown(f"""
            <div class="metric-card" style="background: linear-gradient(135deg, #9b59b6 0%, #8e44ad 100%);">
                <div class="metric-label">Progresso</div>
                <div class="metric-value">{percentage:.0f}%</div>
                <div class="metric-label">{total_evaluated:.1f} de {total_possible:.1f} pts</div>
            </div>
        """, unsafe_allow_html=True)
    
    with col4:
        avaliadas = len(df[~df["Nota"].isna()])
        st.markdown(f"""
            <div class="metric-card" style="background: linear-gradient(135deg, #1abc9c 0%, #16a085 100%);">
                <div class="metric-label">Atividades Avaliadas</div>
                <div class="metric-value">{avaliadas}/{len(df)}</div>
                <div class="metric-label">Pendentes: {len(df[df['Pendente']])}</div>
            </div>
        """, unsafe_allow_html=True)
    
    st.divider()
    
    # ========================================================================
    # SEÇÃO 2: VISUALIZAÇÕES
    # ========================================================================
    
    tab1, tab2, tab3 = st.tabs(["📈 Gráficos", "✏️ Editor de Simulação", "📋 Tabela Detalhada"])
    
    with tab1:
        col1, col2 = st.columns(2)
        
        with col1:
            # Gráfico de distribuição de notas
            st.subheader("Distribuição de Notas")
            
            df_graded = df[~df["Nota"].isna()].copy()
            fig = px.histogram(
                df_graded,
                x="Nota",
                nbins=10,
                title="Frequência de Notas",
                labels={"Nota": "Nota", "count": "Quantidade"},
                color_discrete_sequence=["#667eea"]
            )
            fig.add_vline(
                x=average,
                line_dash="dash",
                line_color="red",
                annotation_text=f"Média: {average:.2f}"
            )
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            # Gráfico de pontos conquistados vs possíveis
            st.subheader("Pontos Conquistados vs Possíveis")
            
            df_points = df.copy()
            df_points["Pontos Conquistados"] = df_points["Nota"] * df_points["Pontos"] / 10
            df_points["Pontos Conquistados"] = df_points["Pontos Conquistados"].fillna(0)
            
            fig = go.Figure(data=[
                go.Bar(
                    name="Conquistados",
                    x=df_points.index,
                    y=df_points["Pontos Conquistados"],
                    marker_color="#2ecc71"
                ),
                go.Bar(
                    name="Possíveis",
                    x=df_points.index,
                    y=df_points["Pontos"],
                    marker_color="#e74c3c",
                    opacity=0.5
                )
            ])
            fig.update_layout(
                title="Pontos por Atividade",
                barmode="overlay",
                xaxis_title="Atividade",
                yaxis_title="Pontos",
                height=400
            )
            st.plotly_chart(fig, use_container_width=True)
        
        col1, col2 = st.columns(2)
        
        with col1:
            # Gráfico de evolução (por atividade)
            st.subheader("Performance por Atividade")
            
            df_sorted = df[~df["Nota"].isna()].sort_values("Nota", ascending=True)
            
            fig = px.bar(
                df_sorted,
                y="Atividade",
                x="Nota",
                orientation="h",
                color="Nota",
                color_continuous_scale="RdYlGn",
                title="Notas por Atividade",
                labels={"Nota": "Nota", "Atividade": ""}
            )
            fig.update_xaxes(range=[0, 10])
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            # Distribuição de status
            st.subheader("Resumo de Status")
            
            status_counts = {
                "Avaliadas": len(df[~df["Nota"].isna()]),
                "Pendentes": len(df[df["Pendente"]])
            }
            
            fig = px.pie(
                values=list(status_counts.values()),
                names=list(status_counts.keys()),
                hole=0.3,
                color_discrete_sequence=["#2ecc71", "#e74c3c"]
            )
            fig.update_layout(title="Status das Atividades")
            st.plotly_chart(fig, use_container_width=True)
    
    with tab2:
        st.subheader("✏️ Simulador de Notas")
        st.markdown("""
            Edite as notas pendentes (marcadas com "-") para simular diferentes cenários.
            A média será recalculada em tempo real!
        """)
        
        # Cria dados editáveis
        df_editable = df.copy()
        df_editable["Nota"] = df_editable["Nota"].round(1)
        
        edited_df = st.data_editor(
            df_editable,
            use_container_width=True,
            key="simulator",
            column_config={
                "Nota": st.column_config.NumberColumn(
                    "Nota (0-10)",
                    min_value=0.0,
                    max_value=10.0,
                    step=0.1,
                    format="%.1f"
                ),
                "Pontos": st.column_config.NumberColumn("Pontos", disabled=True),
                "Status": st.column_config.TextColumn("Status", disabled=True),
                "Atividade": st.column_config.TextColumn("Atividade", disabled=True),
                "Pendente": st.column_config.CheckboxColumn("Pendente", disabled=True)
            }
        )
        
        # Recalcula com dados editados
        sim_average, sim_total_eval, sim_total_poss = calculate_weighted_average(edited_df)
        sim_status = get_approval_status(sim_average, threshold)
        
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric(
                "Simulação - Média Ponderada",
                f"{sim_average:.2f}",
                delta=f"{sim_average - average:.2f}",
                delta_color="off"
            )
        with col2:
            st.metric(
                "Simulação - Status",
                sim_status
            )
        with col3:
            st.metric(
                "Pontos Simulados",
                f"{sim_total_eval:.1f}/{sim_total_poss:.1f}"
            )
        
        if st.button("💾 Salvar Simulação", key="save_sim"):
            st.session_state.edited_data = edited_df
            st.success("✅ Simulação salva com sucesso!")
    
    with tab3:
        st.subheader("📋 Tabela Detalhada de Atividades")
        
        # Coluna de filtro
        col1, col2 = st.columns([0.7, 0.3])
        
        with col1:
            search_term = st.text_input(
                "🔍 Buscar atividade",
                placeholder="Digite para filtrar atividades..."
            )
        
        with col2:
            show_pending_only = st.checkbox("Mostrar apenas pendentes")
        
        # Aplica filtros
        df_display = df.copy()
        
        if search_term:
            df_display = df_display[
                df_display["Atividade"].str.contains(search_term, case=False, na=False)
            ]
        
        if show_pending_only:
            df_display = df_display[df_display["Pendente"]]
        
        # Formata para exibição
        df_display["Status Avaliação"] = df_display["Nota"].apply(
            lambda x: "✅ Avaliada" if pd.notna(x) else "⏳ Pendente"
        )
        df_display["Nota Formatada"] = df_display["Nota"].apply(
            lambda x: f"{x:.1f}/10" if pd.notna(x) else "-"
        )
        df_display["% da Nota"] = (df_display["Nota"] * df_display["Pontos"] / 10).fillna(0).round(2)
        
        # Exibe tabela
        st.dataframe(
            df_display[[
                "Atividade",
                "Status Avaliação",
                "Nota Formatada",
                "Pontos",
                "% da Nota"
            ]].rename(columns={
                "Atividade": "📝 Atividade",
                "Status Avaliação": "📊 Status",
                "Nota Formatada": "⭐ Nota",
                "Pontos": "📌 Peso",
                "% da Nota": "💯 Contribuição"
            }),
            use_container_width=True,
            height=400
        )
    
    st.divider()
    
    # ========================================================================
    # SEÇÃO 3: RESUMO E ANÁLISE
    # ========================================================================
    
    st.header("📊 Análise Detalhada")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("🎯 Insights")
        
        df_graded = df[~df["Nota"].isna()]
        
        if not df_graded.empty:
            max_note = df_graded["Nota"].max()
            min_note = df_graded["Nota"].min()
            mean_note = df_graded["Nota"].mean()
            std_note = df_graded["Nota"].std()
            
            st.info(f"""
            **Estatísticas das Notas Avaliadas:**
            - 🏆 Maior nota: {max_note:.1f}/10
            - 📉 Menor nota: {min_note:.1f}/10
            - 📊 Média simples: {mean_note:.1f}/10
            - 📈 Desvio padrão: {std_note:.2f}
            """)
        
        # Recomendações
        st.info(f"""
        **Recomendações:**
        - Limite de aprovação: {threshold:.1f}
        - Sua média ponderada: {average:.2f}
        - Status: {status}
        
        {"🎉 Você está na frente! Continue assim!" if average >= threshold else "⚠️ Foque em melhorar suas notas para alcançar a aprovação!"}
        """)
    
    with col2:
        st.subheader("📋 Próximos Passos")
        
        pending = df[df["Pendente"]]
        
        if not pending.empty:
            st.warning(f"""
            **Atividades Pendentes: {len(pending)}**
            
            Você ainda tem atividades aguardando avaliação:
            """)
            
            for idx, row in pending.iterrows():
                st.text(f"• {row['Atividade']} ({row['Pontos']:.1f} pts)")
        else:
            st.success("✅ Todas as suas atividades foram avaliadas!")
    
    # ========================================================================
    # RODAPÉ
    # ========================================================================
    
    st.divider()
    st.markdown("""
    <div style="text-align: center; color: #888; font-size: 0.85em;">
    📚 AdaLove - Gestor de Notas | Desenvolvido com ❤️ usando Streamlit<br>
    Última atualização: 2024 | Inteli - Instituto de Tecnologia e Liderança
    </div>
    """, unsafe_allow_html=True)

# ============================================================================
# EXECUÇÃO
# ============================================================================

if __name__ == "__main__":
    main()
