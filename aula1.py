import json
import math
import statistics
from collections import Counter, defaultdict
from dataclasses import dataclass
from datetime import datetime
from typing import Any, Dict, List, Optional, Tuple


def to_float(value: Any) -> Optional[float]:
    if value is None or value == "":
        return None
    if isinstance(value, (int, float)):

        return float(value)
    if isinstance(value, str):
        clean = value.strip().replace("R$", "").replace(".", "").replace(",",".")
        try:
            return float(clean)
        except ValueError:
            return None
    return None


def to_bool(value: Any) -> Optional[bool]:
    if value is None or value == "":
        return None
    
    if isinstance(value, bool):
        return value
    if isinstance(value, (int, float)):
        return bool(value)
    if isinstance(value, str):
        text = value.strip().lower()
        if text in {"true", "1", "sim", "s", "yes", "y"}:
            return True
        if text in {"false", "0", "nao", "não", "no", "n"}:
            return False
    return None

teste_bool = to_bool("no")
# print(teste_bool)

def parse_date(value: Any) -> Optional[str]:
    if value is None or value == "":
        return None
    if isinstance(value, str):
        for fmt in ("%Y-%m-%d", "%d/%m/%Y", "%Y/%m/%d", "%d-%m-%Y"):
            try:
                return datetime.strptime(value, fmt).strftime("%Y-%m-%d")
            except ValueError:
                continue
        return value
    return None

teste= parse_date("2026/04/27")
print(teste)


def load_json(path: str) -> Dict[str, Any]:
    with open(path, 'r', encoding='utf-8') as f:
        return json.load(f)
    
def save_json(path: str, data: Dict[str, Any]) -> None:
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(data,f, ensure_ascii=False, indent=2)

teste=load_json("teste.json")
# print(teste)

def infer_field_type(values: List[Any]) -> str:
    not_null = [v for v in values if v is not None and v != ""]
    if not not_null:
        return "indefinido"
    numeric = sum(1 for v in not_null if isinstance(v , (int, float)) or to_float(v) is not None)
    if numeric == len(not_null):
        unique = len(set(float(to_float(v)) for v in not_null if to_float(v) is not None))
        if unique <= 12:
            return "quantitativa_discreta"
        return "quantitava_continua"
    unique = len(set(str(v) for v in not_null))
    if unique <= 12:
            return "quantitativa_nominal"
    return "quantitativa_ordinal_ou_textual"

print(infer_field_type(['verde', 'azul', 'castanho']))

# Essa função gera um relatório de valores nulos (ou vazios) em uma lista de registros
# (dicionários). Ela conta quantos campos estão “faltando” em cada chave.
def null_report(records: List[Dict[str, Any]]) -> Dict[str, int]:
    # Função que conta valores nulos ou vazios em cada campo
    # records = lista de dicionários (tipo linhas de uma tabela)
    # retorna um dicionário com contagem de nulos por coluna
    counts: Dict[str, int] = Counter()  # counts deve se comportar como dicionário com chaves do tipo str e valores do tipo int
    # Counter é um tipo especial de dicionário usado para contar ocorrências.
    # Cria um contador vazio para armazenar quantos nulos cada chave tem
    for rec in records:   # Percorre cada registro (cada "linha" de dados)
        for k, v in rec.items():  # Percorre cada campo (chave e valor) dentro do registro
            # k recebe a chave (key)
            # v recebe o valor (value) associado a essa chave
            if v is None or v == "":  # Verifica se o valor está vazio (None ou string vazia)
                counts[k] += 1    # Incrementa 1 na contagem daquela chave
    return dict(counts)   # Converte o Counter para dict normal e retorna
# dict(counts) pega o objeto counts (que no seu caso é um Counter) e converte para um dicionário comum (dict).


# Esse código define uma classe chamada PreparedData, mas na forma atual ela está sendo usada como um
# “container de dados” (data structure) — ou seja, não tem lógica, só organiza informações.
# @dataclass é um decorador do Python (do módulo dataclasses) que serve para criar classes focadas em armazenar
# dados sem precisar escrever muito código repetitivo.
# Um decorador em Python é uma forma de modificar ou estender o comportamento
# de uma função ou classe sem alterar o código original dela.
# Ele é basicamente uma função que “envolve” outra função.

@dataclass
class PreparedData:
    negocio: Dict[str, Any]
    transacoes: List[Dict[str, Any]]
    dias: List[Dict[str, Any]]
    recepcao: Dict[str, Any]

# Esse trecho define uma classe chamada InsightCalculadoEngine, que parece ser o
# “motor” responsável por processar dados e gerar insights.
class InsightCalculadoEngine:
    def __init__(self, data: Dict[str, Any]):
        # self representa a própria instância do objeto que está sendo criada ou usada
        self.raw = data                            # guarda os dados originais
        self.prepared = self._prepare_data(data)   # chama o método da própria classe e salva o resultado em prepared

    # --------------------------------------------------------
    # Preparação
    # --------------------------------------------------------
    # Esse método _prepare_data é o coração do processamento de dados da sua classe. Ele pega
    # dados brutos e transforma em um formato limpo, padronizado e pronto para análise.
    def _prepare_data(self, data: Dict[str, Any]) -> PreparedData:
        negocio = data.get("negocio", {})
        dados = data.get("dados", {})
        recepcao = data.get("recepcao", {})
        # dict.get(chave, valor_padrao):
        # retorna o valor da chave se ela existir
        # se não existir, retorna o valor_padrao (em vez de dar erro)
        # se não existir, retorna {} (dicionário vazio)

        transacoes = []   # criando lista vazia
        for item in dados.get("transacoes",[]):     # [] retorna uma lista vazia
            record = dict(item)                     # cria um dicionário (dict) a partir de item.
            record["data"] = parse_date(record.get("data"))  # trata o formato de data
            if "valor" in record:
                record["valor"] = to_float(record.get("valor"))     # trata float
            if "pago_no_prazo" in record:
                record["pago_no_prazo"] = to_bool(record.get("pago_no_prazo"))   # trata boolean
            if "desconto" in record:
                record["desconto"] = to_float(record.get("desconto"))    # trata float
            if "marketing" in record:
                record["marketing"] = to_float(record.get("marketing"))  # trata float
            transacoes.append(record)     # adicionando na lista

        dias = []    # criando lista vazia
        for item in dados.get("dias", []):
            record = dict(item)
            record["data"] = parse_date(record.get("data"))
            for field in ["receita", "despesa", "vendas_qtd", "clientes", "marketing", "desconto_medio"]:
                if field in record:  # verifica se a chave field existe dentro do dicionário record
                    record[field] = to_float(record.get(field))   # trata float
            dias.append(record)

        if not dias and transacoes:
            dias = self._derive_daily_records(transacoes)

        return PreparedData(negocio=negocio, transacoes=transacoes, dias=dias, recepcao=recepcao)


 # Esse método aula_1 é basicamente uma função de “análise exploratória inicial” (EDA) do seu sistema.
    # Ele organiza informações básicas do dataset para responder: “o que eu tenho de dados aqui?”
    def aula_1(self) -> Dict[str, Any]:   # Define o método "aula_1", que retorna um dicionário com análises iniciais dos dados
        transacoes = self.prepared.transacoes   # Extrai a lista de transações já preparadas
        dias = self.prepared.dias               # Extrai a lista de registros diários já preparados
        if transacoes:                          # Verifica se existem transações
            keys = sorted({k for rec in transacoes for k in rec.keys()})      # sorted transforma o set em uma lista ordenada
            # Cria um conjunto com todas as chaves existentes nas transações
            # Depois converte em lista ordenada
            # Ex: ["valor", "data", "tipo", "cliente"]
            classificacao = {}    # Inicializa dicionário que armazenará o tipo de cada campo
            for key in keys:      # Itera sobre cada campo existente nas transações
                valores = [rec.get(key) for rec in transacoes]   # Coleta todos os valores daquele campo em todas as transações
                classificacao[key] = infer_field_type(valores)
                # Usa uma função que infere o tipo do campo
                # Ex: quantitativa, qualitativa, etc.
        else:   # Caso não existam transações
            classificacao = {}    # Define classificação vazia

        sample_size = min(5, len(transacoes))   # Define tamanho da amostra (no máximo 5 registros)
        amostra = transacoes[:sample_size]      # Pega os primeiros registros como amostra

        return {  # Retorna um relatório estruturado com análises da "aula 1"
            "tema": "Entender os dados do negócio",  # Define o objetivo da análise
            # Descreve o problema de negócio em linguagem simples
            "problema_financeiro": "O empreendedor possui dados, mas não sabe o que está registrando nem como organizar isso para análise.",
            "calculos": {  # Seção com métricas e cálculos
                "populacao_transacoes": len(transacoes),    # Quantidade total de transações
                "populacao_registros_diarios": len(dias),   # Quantidade total de registros diários
                "amostra_exibida": sample_size,             # Quantidade de registros mostrados na amostra
                "classificacao_campos_transacoes": classificacao,        # Tipos de cada campo das transações
                "campos_faltantes_transacoes": null_report(transacoes),  # Conta valores nulos/vazios nas transações
                "campos_faltantes_dias": null_report(dias),  # Conta valores nulos/vazios nos dados diários
                "amostra_transacoes": amostra,               # Exibe amostra dos dados
            },
            "insights": [ # Lista de interpretações automáticas
                # Explica o objetivo da análise de tipos
                "Nesta etapa o sistema identifica quais campos são qualitativos e quais são quantitativos.",
                # Explica que o sistema detecta problemas nos dados
                "Também aponta lacunas iniciais para preparar a análise exploratória das próximas aulas.",
            ],
        }
    
dados_empresas = load_json("exemplo_entrada_insight_calculado.json")
engine = InsightCalculadoEngine(dados_empresas)
resultado = engine.aula_1()
print("\nTeste 2 - aula1")
print(resultado)
save_json("teste_saida_aulalc.json", resultado)
    

        
        


