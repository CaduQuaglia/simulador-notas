"""
Script de Exemplo - Gerador de Dados para Teste
Cria um arquivo CSV com dados de exemplo para testar a aplicação
"""

import pandas as pd
import csv

# Dados de exemplo
exemplo_dados = {
    "Atividade": [
        "Business Question 1",
        "[GRADED ACTIVITY] Gitflow Workflow",
        "PROJECT AND BUSINESS UNDERSTANDING",
        "FUNCTIONAL AND NON-FUNCTIONAL REQUIREMENTS SPECIFICATION",
        "EVOLUTIONARY PROJECT MANAGEMENT AND CONFIGURATION MANAGEMENT",
        "Differentiation and its applications (functions of one variable)",
        "[GRADED ACTIVITY] Stakeholder Map",
        "TECHNICAL SOLUTION (DESIGN)",
        "DATA MODELING",
        "SERVICE BLUEPRINT",
        "EVOLUTIONARY PROJECT MANAGEMENT",
        "[GRADED ACTIVITY] Elaboration of an Application Integrated with a Database",
        "PROJECT DEVELOPMENT",
        "[GRADED ACTIVITY] Software Test Case",
        "TECHNICAL INFRASTRUCTURE AND DEPLOYMENT MAPPING",
        "[GRADED ACTIVITY] Maze Explorer: Stacks and Queues",
        "DATABASE IMPLEMENTATION",
        "Business Question 2"
    ],
    "Status": [
        "Feito", "Feito", "Feito", "Feito", "Feito",
        "Feito", "Feito", "Feito", "Feito", "Feito",
        "Feito", "Feito", "Feito", "Feito", "Feito",
        "Feito", "Feito", "Feito"
    ],
    "Pontos": [
        2, 4, 3, 2, 3, 3, 3, 3, 3, 2, 2, 3, 3, 2, 2, 3, 2, 2
    ],
    "Nota": [
        5.0, 8.5, 6.0, 6.4, 6.8, 8.5, 8.5, 5.4, 5.1, 5.1, 5.0, 5.6, 8.2, 6.5, 9.0, 7.5, 8.6, 5.0
    ],
    "Pendente": [
        False, False, False, False, False,
        False, False, False, False, False,
        False, False, False, False, False,
        False, False, False
    ]
}

# Criar DataFrame
df = pd.DataFrame(exemplo_dados)

# Salvar como CSV
df.to_csv("exemplo_notas.csv", index=False, encoding="utf-8")

print("✅ Arquivo 'exemplo_notas.csv' criado com sucesso!")
print("\nPreview dos dados:")
print(df.to_string(index=False))
print(f"\nTotal de atividades: {len(df)}")
print(f"Total de pontos: {df['Pontos'].sum()}")

# Cálculo de média ponderada para verificação
def calcular_media(df):
    evaluated = df[~df["Nota"].isna()].copy()
    if evaluated.empty or evaluated["Pontos"].sum() == 0:
        return 0.0
    weighted_sum = (evaluated["Nota"] * evaluated["Pontos"]).sum()
    total_points = evaluated["Pontos"].sum()
    return weighted_sum / total_points

media = calcular_media(df)
print(f"Média ponderada (verificação): {media:.2f}")
