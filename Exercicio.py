# Dados simulados do Instituto Saber Social
assistidos = [
    {"nome": "Ana", "frequencia": 85, "oficina": "Informática"},
    {"nome": "Carlos", "frequencia": 60, "oficina": "Artes"},
    {"nome": "Mariana", "frequencia": 92, "oficina": "Informática"}
]

# Função para validar e consultar dados (com parâmetro opcional)
def filtrar_elegiveis(lista, freq_minima=75):
    return [a for a in lista if a["frequencia"] >= freq_minima]

# Função para o processamento principal (com parâmetro opcional)
def processar_auxilio(lista_filtrada, valor_base=150.0):
    total = sum(valor_base + (50.0 if a["frequencia"] >= 90 else 0) for a in lista_filtrada)
    return {"quantidade": len(lista_filtrada), "total_auxilio": total}

# Função para apresentar os resultados (com parâmetro opcional)
def exibir_relatorio(res, titulo="RELATÓRIO DE IMPACTO"):
    print(f"=== {titulo} ===")
    print(f"Assistidos Elegíveis: {res['quantidade']}")
    print(f"Investimento Total: R$ {res['total_auxilio']:.2f}")

# Execução: Chamada de função que utiliza o resultado de outra
elegiveis = filtrar_elegiveis(assistidos)      
resultado = processar_auxilio(elegiveis)       
exibir_relatorio(resultado)                    