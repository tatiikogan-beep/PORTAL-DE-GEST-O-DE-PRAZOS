# -*- coding: utf-8 -*-
"""
IGSA · Gestão de Prazos Preclusivos — Imaculada Gordiano Sociedade de Advogados
Controladoria Jurídica

App Streamlit único. UI redesenhada (barra lateral vinho/dourado, Visão Geral com
dois layouts, cards, gráficos limpos e tabela "Prazos por responsável") sobre o
pipeline de dados real (upload LegalOne .xlsx → validação → seleção de coordenador
→ publicação com commit no GitHub → exportações openpyxl).

Toda a lógica de negócio segue o "Manual de Configuração — Revisão 2 (Junho/2026)".
Os pontos de configuração citados no manual (seção 18) estão reunidos no bloco
CONSTANTES abaixo.
"""
import streamlit as st
import pandas as pd
import numpy as np
import json, re, io, os, base64, unicodedata
from datetime import datetime, date

import openpyxl
from openpyxl.styles import PatternFill, Font, Alignment
from openpyxl.utils import get_column_letter

st.set_page_config(
    page_title="IGSA · Gestão de Prazos",
    page_icon="⚖️",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ════════════════════════════════════════════════════════════════════════════
# CONSTANTES — configurações do manual (seção 18: editar aqui)
# ════════════════════════════════════════════════════════════════════════════

# 18-A/B · Mapa coordenador → executores (o coordenador também é executor de si).
# Variações de acento listadas nas duas grafias (o LegalOne às vezes exporta sem acento).
COORD_MAP = {
    "ARMANDO HÉLIO ALMEIDA MONTEIRO DE MORAES": [],
    "CARMEN MARIA HOLANDA DE LIMA": ["ANTONIO JOSE ANDRADE DA SILVA JUNIOR"],
    "GABRIEL GIORGIO CICCHELERO": [
        "ARMANDO HÉLIO ALMEIDA MONTEIRO DE MORAES", "IRENE FLÁVIA SERENÁRIO",
        "ALEXIA ALENCAR CAPIBARIBE", "ALYSSON NARBAL DE OLIVEIRA SOMBRA",
        "ANDREZA DE ARAÚJO DIAS", "DIOGO HENRIQUE DE ARAÚJO FILHO",
        "JULIANA DE OLIVEIRA ROCHA", "RAFAEL CAVALCANTE BARBOSA", "GABRIEL GIORGIO CICCHELERO"],
    "JENIFFER ROSA BARBOSA DE SALES": ["GABRIEL BERTACCO HADDAD", "JENIFFER ROSA BARBOSA DE SALES"],
    "JULIANA MIRELLA ALVES RODRIGUES": [
        "ARTHUR MASSARI", "DANIEL BARROS DE OLIVEIRA", "GUSTAVO LOPES ALENCAR FILHO",
        "KELIANE DE OLIVEIRA", "MONIQUE DE KAROLIN SILVA DA COSTA", "NATALIA PAIVA DE PAULA",
        "ROBERTA RAYANNE VASCONCELOS BOTO", "ROBERTA FURTADO DE ARRAES ALENCAR E CASTRO",
        "TATIANE CARMO SANTA ROSA", "THALLYS ANDERSON FERREIRA DE LIMA",
        "VICTOR EMANOEL FRADIQUE ACCIOLY FONTENELE", "JULIANA MIRELLA ALVES RODRIGUES"],
    "KARYNA SARAIVA LEÃO GAYA": ["KARYNA SARAIVA LEÃO GAYA"],
    "MARCELLE LEITE RENTROIA": ["MARIANA MOTA FROTA", "MARCELLE LEITE RENTROIA"],
    "MARIA IMACULADA GORDIANO OLIVEIRA BARBOSA": ["MARIA IMACULADA GORDIANO OLIVEIRA BARBOSA"],
    "NAYANDERSON LUAN MELLO PINHEIRO": [
        "ANDRE VIANA GARRIDO", "EMERSON TRAVASSOS TORQUATO", "NAYANDERSON LUAN MELLO PINHEIRO"],
    "RONALD FEITOSA AGUIAR FILHO": ["RONALD FEITOSA AGUIAR FILHO"],
    "SUZANA MARIA CAMPOS MARANHÃO DE LIMA": [
        "GIOVANNA CAMPOS PEREIRA", "MATHEUS CAVALCANTI DE ARAUJO",
        "SUZANA MARIA CAMPOS MARANHÃO DE LIMA", "SUZANA MARIA CAMPOS MARANHAO DE LIMA"],
    "TARCILLA GOES BARBOSA": ["TARCILLA GOES BARBOSA"],
    "TICIANNA PIRES DE SOUZA": ["TICIANNA PIRES DE SOUZA"],
    "YURI ALVES BARROS DOS SANTOS": [
        "CAMILLA GOES BARBOSA", "YURI ALVES BARROS DOS SANTOS", "ALANIS ALVES DE SOUSA",
        "JÚLIA MENEZES MORGADO"],
    "YURI GONDIM DE AMORIM": ["YURI GONDIM DE AMORIM"],
    # Controladoria (uso interno/admin — não faz parte do organograma jurídico acima).
    "TATIANA KOGAN": ["VANESSA NUNES HOLANDA"],
}
# Coordenador exibido com nome alternativo no painel (seção 7).
COORD_DISPLAY = {"TATIANA KOGAN": "CONTROLADORIA JURÍDICA"}

# Observação (manual §9 / 18-C): o conceito de "responsáveis inativos" foi
# DESCONTINUADO a pedido da Controladoria. Não há filtro por status de responsável
# nem pela coluna Status da planilha — todo registro dentro do recorte de datas entra.

# 18-D · Responsáveis/coordenadores excluídos de TODAS as visualizações públicas
# (Visão Geral, Por Coordenação, Auditoria e Exportação) — seção 10. Todas as grafias.
# Os registros continuam armazenados na base; só ficam fora de telas, gráficos e relatórios.
EXCLUDED_SET = {
    "TATIANA KOGAN", "APARECIDO", "MARIA LAURA MELO ALMEIDA", "YURI GONDIM DE AMORIM",
}
# 18-E · Coordenações inteiramente ocultas do painel público (seção 11).
HIDDEN_COORDS = {"TATIANA KOGAN"}

# Seção 2 · Colunas obrigatórias da planilha exportada do LegalOne.
# A coluna de tipo pode vir como "Tipo" (antiga) ou "Tipo - Subtipo" (nova) — ver TIPO_COLS.
COLUNAS_ESPERADAS = ["Id", "Tipo", "Descrição", "Conclusão prevista",
                     "Responsável processo", "Pasta", "Status"]

# 18-G · Feriados nacionais 2026 (seção 4). Carnaval/Corpus Christi NÃO entram.
# Ao virar o ano, duplique esta lista com o novo ano e atualize HOLIDAYS_NP.
HOLIDAYS_2026 = ["2026-01-01", "2026-04-21", "2026-05-01", "2026-09-07",
                 "2026-10-12", "2026-11-02", "2026-11-15", "2026-12-25"]
HOLIDAYS_NP = np.array(HOLIDAYS_2026, dtype="datetime64[D]")

# 18-H · Horizonte do filtro de datas (seção 3). Padrão do manual: DU <= 1.
#   DU_LIMIT = 1  → inclui vencidos (<0) + hoje (0) + D-1 (1)   [padrão]
#   DU_LIMIT = 0  → apenas vencidos + hoje
#   DU_LIMIT = 2  → amplia para dois dias úteis à frente
DU_LIMIT = 1

# 18-I · Repositório GitHub de publicação.
GITHUB_REPO = "tatiikogan-beep/Gestao-Prazos-IGSA"

DATA_FILE = "dados_publicados.json"


def saved_gh_token():
    """Token salvo nos Secrets do Streamlit Cloud (Manage app → Settings → Secrets,
    chave GITHUB_TOKEN). Evita ter que colar o token manualmente a cada carga/limpeza."""
    try:
        return st.secrets.get("GITHUB_TOKEN", "")
    except Exception:
        return ""

# Vínculos responsável→coordenador aprendidos na Área Administrativa (seção 8):
# quando alguém sem coordenador mapeado recebe um coordenador manualmente, o
# vínculo é gravado aqui e passa a valer para todas as cargas seguintes.
LEARNED_COORD_FILE = "coord_aprendido.json"

# Correções de nome de responsável (ex.: grafia divergente no LegalOne) e
# responsáveis marcados para NUNCA importar — ambos definidos na seção 2 da
# Área Administrativa e válidos para todas as cargas seguintes.
LEARNED_NAME_FILE = "nomes_corrigidos.json"
LEARNED_EXCLUDE_FILE = "responsaveis_nao_importar.json"

# Rótulo especial para responsáveis sem vínculo de coordenador (seções 6/8).
SEM_COORD = "SEM COORDENADOR"

# Índice reverso executor → coordenador (derivado do COORD_MAP + aprendizado automático).
RESP_TO_COORD = {}
for _coord, _members in COORD_MAP.items():
    for _m in _members:
        RESP_TO_COORD[_m] = _coord
if os.path.exists(LEARNED_COORD_FILE):
    try:
        with open(LEARNED_COORD_FILE, encoding="utf-8") as _f:
            RESP_TO_COORD.update(json.load(_f))
    except Exception:
        pass

NOME_CORRECTIONS = {}
if os.path.exists(LEARNED_NAME_FILE):
    try:
        with open(LEARNED_NAME_FILE, encoding="utf-8") as _f:
            NOME_CORRECTIONS = json.load(_f)
    except Exception:
        pass

NAO_IMPORTAR = set()
if os.path.exists(LEARNED_EXCLUDE_FILE):
    try:
        with open(LEARNED_EXCLUDE_FILE, encoding="utf-8") as _f:
            NAO_IMPORTAR = set(json.load(_f))
    except Exception:
        pass

# ---- Paleta (design system vinho/dourado) ----
CLR_HEADER = "7E1F2D"; CLR_HEADER_TXT = "FFFFFF"
CLR_VERDE = "C6EFCE"; CLR_AMARELO = "FFEB9C"
CLR_ROSA = "FFC7CE"; CLR_VERM = "FFDDB3"; CLR_VERM_TXT = "000000"   # seção 13: DU<0 = laranja bem claro
CLR_GOLD = "CDA736"; CLR_GOLD_TXT = "FFFFFF"

WINE = "#7E1F2D"; WINE_DARK = "#641828"; WINE_LIGHT = "#9B2335"
GOLD = "#CDA736"; GOLD_DARK = "#8E6E1C"; INK = "#2A2420"; SAND = "#F7F2E9"
GREEN = "#2E9E5B"
WINE_COLORS = ["#641828", "#7E1F2D", "#9B2335", "#B83A4C", "#C85A6A", "#D97A88", "#E8A0A8"]
MULTI_COLORS = ["#7E1F2D", "#CDA736", "#2E9E5B", "#BE5862", "#8E6E1C", "#651823",
                "#43B26C", "#D8868E", "#9E3340", "#B08A26"]

TIPOS_CONHECIDOS = ["Prazo", "Audiência", "Diversos", "Pauta de Julgamento", "Perícia", "Publicação"]

# Mapa Tipo-base → tipo normalizado (seção 12). O valor bruto vem como "Tipo - Subtipo".
# O tipo-base é a parte antes do 1º hífen (o base nunca contém hífen); o subtipo é o resto.
TIPO_BASE_MAP = {
    "Prazo": "Prazo", "Audiência": "Audiência", "Diversos": "Diversos",
    "Diligência externa": "Diversos", "Serviço": "Diversos", "Workflow": "Diversos",
    "Pauta de Julgamento": "Pauta de Julgamento", "Perícia": "Perícia", "Publicação": "Publicação",
}
# Colunas que podem trazer o tipo (a exportação nova usa "Tipo - Subtipo").
TIPO_COLS = ("Tipo - Subtipo", "Tipo")


# ════════════════════════════════════════════════════════════════════════════
# HELPERS
# ════════════════════════════════════════════════════════════════════════════
def fmt_num(n):
    try:
        return f"{int(n):,}".replace(",", ".")
    except (TypeError, ValueError):
        return str(n)


def busdays(d_from, d_to):
    """Dias úteis entre duas datas, excluindo fins de semana e feriados nacionais."""
    try:
        return int(np.busday_count(np.datetime64(d_from, "D"),
                                   np.datetime64(d_to, "D"), holidays=HOLIDAYS_NP))
    except Exception:
        return None


def parse_date(val):
    if val is None:
        return None
    if isinstance(val, (datetime, date)):
        return val.date() if isinstance(val, datetime) else val
    s = str(val).strip()
    if s in ("", "nan", "NaT", "None"):
        return None
    for f in ["%Y-%m-%d", "%d/%m/%Y", "%d.%m.%Y", "%Y-%m-%d %H:%M:%S"]:
        try:
            return datetime.strptime(s[:len(f) if "%H" not in f else 19], f).date()
        except Exception:
            pass
    try:
        return pd.to_datetime(s, dayfirst=True).date()
    except Exception:
        return None


def normalizar_tipo(tipo):
    """
    Normaliza o valor bruto 'Tipo - Subtipo' do LegalOne (seção 12).
    Regra: tipo-base (antes do 1º hífen) define o tipo, EXCETO
    'Workflow - Protocolo (...)' que vira Prazo. Base desconhecida → Diversos.
    """
    base, _, sub = str(tipo).partition("-")
    base = base.strip()
    sub = sub.strip()
    if base == "Workflow" and sub.lower().startswith("protocolo"):
        return "Prazo"
    return TIPO_BASE_MAP.get(base, "Diversos")


def extract_fatal(desc):
    if not isinstance(desc, str):
        return None
    m = re.search(r"FATAL[\s:]+(\d{2})/(\d{2})/(\d{4})", desc, re.IGNORECASE)
    if m:
        try:
            return date(int(m.group(3)), int(m.group(2)), int(m.group(1)))
        except Exception:
            pass
    return None


def extract_aud(desc):
    if not isinstance(desc, str):
        return None
    m = re.search(r"AUD[\s:]+(\d{2})/(\d{2})/(\d{4})", desc, re.IGNORECASE)
    if m:
        try:
            return date(int(m.group(3)), int(m.group(2)), int(m.group(1)))
        except Exception:
            pass
    return None


def proximo_dia_util(ref):
    """Próximo dia útil após `ref` — usado quando a descrição não traz uma
    data FATAL/AUD explícita e a Conclusão prevista representa o D-1
    (o dia de agir), não a data fatal em si."""
    d = np.busday_offset(np.datetime64(ref.strftime("%Y-%m-%d"), "D"), 1,
                         roll="forward", holidays=HOLIDAYS_NP)
    return date.fromisoformat(str(d))


def _sem_acento(s):
    nfd = unicodedata.normalize("NFD", str(s or "").upper())
    return "".join(c for c in nfd if unicodedata.category(c) != "Mn")


def tem_termo_julgamento(desc):
    """Descrições de acompanhamento de julgamento não têm data fatal — ficam
    sempre "dentro do prazo", independente de qualquer data cadastrada."""
    d = _sem_acento(desc)
    return "AUDIENCIA DE JULGAMENTO" in d or "ACOMPANHAR JULGAMENTO" in d


def check_incons(tipo, desc, conclusao, fatal, aud):
    """Regras de validação da seção 15. Retorna alertas separados por '; '.
    Atividades do tipo Diversos ficam fora da análise de inconsistências."""
    if tipo == "Diversos":
        return ""
    issues = []
    d = desc or ""
    ref = fatal or aud                      # FATAL tem prioridade sobre AUD
    # Regra 1 — conclusão posterior à data da descrição. Não se aplica a
    # "Pauta de Julgamento" (a data da descrição é só a sessão, não limita a
    # conclusão). Tolera 1 dia útil de diferença: quando a data da descrição
    # cai numa sexta-feira (ou antes de feriado), a conclusão cair no próximo
    # dia útil (segunda-feira) é o comportamento esperado, não um erro.
    if tipo != "Pauta de Julgamento" and ref and conclusao and conclusao > ref:
        gap = busdays(ref, conclusao)
        if gap is None or gap > 1:
            issues.append(f"Conclusão posterior à data da descrição ({ref.strftime('%d/%m/%Y')})")
    # Regra 2 — ano com 5+ dígitos dentro de uma data (dd/mm/AAAAA), só nestes
    # tipos. Exige o padrão de data (duas barras antes do ano) para não pegar
    # números de processo/protocolo/registro que também têm 5+ dígitos mas
    # não são datas (ex.: "355054-REQ", "0011212-77.2026...", nº de LO/SPU).
    if tipo in ("Prazo", "Audiência", "Pauta de Julgamento", "Perícia") and \
            re.search(r"\d{1,2}/\d{1,2}/\d{5,}", d):
        issues.append("Ano inválido na descrição")
    # Regra 3 — Prazo com descrição de Audiência
    if tipo == "Prazo" and re.search(r"AUDIÊNCIA DE CONCILIAÇÃO", d, re.IGNORECASE):
        issues.append("Tipo Prazo com descrição de Audiência")
    # Regra 4 — Audiência com descrição de Prazo
    if tipo == "Audiência" and re.search(r"PRAZO.*Protocolar", d, re.IGNORECASE):
        issues.append("Tipo Audiência com descrição de Prazo")
    return "; ".join(issues)


def get_row_color(du, tipo):
    """Cor da linha (seção 13). Usado em tabelas e Excel (fora da Auditoria —
    que tem sua própria cor fixa para inconsistências). Descrições de
    acompanhamento de julgamento já chegam aqui com "du" forçado para verde
    (ver construir_registros / tem_termo_julgamento)."""
    if du is None:
        return None, None
    if du < 0:
        return CLR_VERM, CLR_VERM_TXT                                # P3 · DU<0 vermelho claro
    if du == 0:
        return CLR_ROSA, "000000"                                    # DU=0 rosa
    if du == 1:
        return CLR_AMARELO, "000000"                                 # DU=1 amarelo
    return CLR_VERDE, "000000"                                       # DU>1 verde


def abbrev_name(name):
    """Abrevia nome mantendo primeiro + último sobrenome relevante (para colunas proporcionais)."""
    if not name:
        return name
    up = str(name).strip()
    if up.upper() in ("CONTROLADORIA JURÍDICA", SEM_COORD, "(SEM RESPONSÁVEL)"):
        return name
    conn = {"de", "da", "do", "dos", "das", "e"}
    suf = {"filho", "júnior", "junior", "jr", "jr.", "neto", "sobrinho", "segundo"}
    parts = up.split()
    if len(parts) <= 2:
        return name
    first = parts[0]
    last = parts[-1]
    if last.lower() in suf:
        j = len(parts) - 2
        if parts[j].lower() in conn and j > 0:
            j -= 1
        last = parts[j] + " " + last
    return first + " " + last


# ════════════════════════════════════════════════════════════════════════════
# PROCESSAMENTO DE DADOS (seções 2, 3, 5, 6, 12, 15, 16)
# ════════════════════════════════════════════════════════════════════════════
def processar_planilha(uploaded_file):
    """Lê a planilha; cabeçalho na 2ª linha (linha 0 = info de exportação)."""
    df_raw = pd.read_excel(uploaded_file, sheet_name=0, header=None)
    header_idx = 1
    for i in range(min(10, len(df_raw))):
        row = df_raw.iloc[i].tolist()
        if any(("Conclusão" in str(c)) or ("Tipo" == str(c).strip()) for c in row):
            header_idx = i
            break
    headers = [str(h).strip() for h in df_raw.iloc[header_idx].tolist()]
    df = df_raw.iloc[header_idx + 1:].copy()
    df.columns = headers
    df = df.drop_duplicates().reset_index(drop=True)
    return df, headers


def validar_estrutura(headers):
    faltando = []
    for c in COLUNAS_ESPERADAS:
        if c == "Tipo":
            if not any(t in headers for t in TIPO_COLS):   # aceita "Tipo" ou "Tipo - Subtipo"
                faltando.append("Tipo / Tipo - Subtipo")
        elif c not in headers:
            faltando.append(c)
    return faltando


def _get(row, *names, default=""):
    for n in names:
        if n in row and pd.notna(row[n]):
            v = str(row[n]).strip()
            if v not in ("", "nan", "None", "NaT"):
                return v
    return default


def _primeiro_nome_valido(texto):
    """'Responsável processo' e 'Envolvidos / Nome' às vezes vêm com mais de um
    nome concatenado (ex.: "NOME A;\nNOME B"). Prioriza o primeiro nome que já
    tenha coordenador cadastrado; se nenhum bater, usa o primeiro da lista."""
    candidates = [n.strip() for n in re.split(r"[;,|\n]", texto) if n.strip()]
    if not candidates:
        return ""
    mapped = next((c for c in candidates if c in RESP_TO_COORD), None)
    return mapped if mapped else candidates[0]


def resolver_responsavel(row):
    """Responsável + fallback para 'Envolvidos / Nome' (seção 6)."""
    resp = _get(row, "Responsável processo", "Responsavel processo")
    if resp:
        return _primeiro_nome_valido(resp)
    env = _get(row, "Envolvidos / Nome")
    if env:
        return _primeiro_nome_valido(env)
    return ""


def construir_registros(df, today, coord_overrides=None, resp_corrections=None, resp_excluir=None):
    """
    Constrói registros aplicando todas as regras do manual.
    coord_overrides: {responsável: coordenador} escolhido manualmente na carga (seção 8).
    resp_corrections: {nome digitado: nome corrigido} escolhido manualmente na carga (seção 8).
    resp_excluir: {responsáveis} marcados para não importar nesta carga (seção 8).
    Retorna (registros, sem_coord_map, stats, registros_futuros) — sem_coord_map =
    {resp: qtd} não mapeados. Cada registro carrega seu próprio campo "incons"
    (usado pelas abas Auditoria e Revisão de Prazos Futuros).
    registros_futuros: mesmos dados/regras de "registros", mas para DU > DU_LIMIT
    (fora do recorte principal) — usado só pela aba "Revisão de Prazos Futuros"
    (seção 19). Não altera stats/sem_coord_map/registros em nada: é somente
    aditivo, para não interferir nas demais abas.
    """
    coord_overrides = coord_overrides or {}
    resp_corrections = resp_corrections or {}
    resp_excluir = resp_excluir or set()
    registros, seen = [], set()
    registros_futuros, seen_futuro = [], set()
    sem_coord_map = {}
    # Transparência (nenhum registro sai silenciosamente): contadores de descartes.
    stats = {"sem_data": 0, "fora_recorte": 0, "duplicatas": 0, "nao_importados": 0}
    for _, row in df.iterrows():
        conclusao = parse_date(row.get("Conclusão prevista"))
        if not conclusao:
            stats["sem_data"] += 1
            continue

        tipo = normalizar_tipo(_get(row, *TIPO_COLS))   # seção 12 (lê "Tipo - Subtipo" ou "Tipo")
        desc = _get(row, "Descrição")
        fatal = extract_fatal(desc)
        aud = extract_aud(desc)

        # Para "Prazo", a Conclusão prevista é o D-1 (dia de agir), não a data
        # fatal em si — a data fatal real vem da descrição (FATAL:/AUD:) ou,
        # na ausência dela, é o próximo dia útil após a Conclusão prevista.
        # Acompanhamento de julgamento não tem data fatal: fica sempre dentro
        # do prazo. Para os demais tipos, a Conclusão prevista já é a data.
        forcar_dentro = tipo == "Prazo" and tem_termo_julgamento(desc)
        if forcar_dentro:
            du = DU_LIMIT + 1
        elif tipo == "Prazo":
            du = busdays(today, fatal or aud or proximo_dia_util(conclusao))
        else:
            du = busdays(today, conclusao)
        if du is None:
            stats["sem_data"] += 1
            continue

        id_ = _get(row, "Id")
        pasta = _get(row, "Pasta")
        processo = pasta if pasta else id_              # seção 5
        resp = resolver_responsavel(row)                # seção 6
        # Correção de grafia (persistida + desta carga) e exclusão manual
        # de importação (seção 2/8 da Área Administrativa).
        resp = NOME_CORRECTIONS.get(resp, resp_corrections.get(resp, resp))
        excluido_manual = resp in NAO_IMPORTAR or resp in resp_excluir

        if not forcar_dentro and du > DU_LIMIT:         # seção 3 / 18-H — fora do horizonte (futuro)
            stats["fora_recorte"] += 1
            if excluido_manual:
                continue
            key_f = f"{id_}|{conclusao.isoformat()}|{tipo}|{resp}"
            if key_f in seen_futuro:
                continue
            seen_futuro.add(key_f)
            resp_disp = resp or "(Sem responsável)"
            coord_raw = RESP_TO_COORD.get(resp, coord_overrides.get(resp, SEM_COORD))
            coord_display = COORD_DISPLAY.get(coord_raw, coord_raw)
            incons = check_incons(tipo, desc, conclusao, fatal, aud)
            registros_futuros.append({
                "id": id_, "processo": processo, "tipo": tipo, "desc": desc[:300],
                "status": _get(row, "Status"), "resp": resp_disp,
                "coord": coord_raw, "coord_display": coord_display,
                "conclusao": conclusao.strftime("%d/%m/%Y"), "conclusao_iso": conclusao.isoformat(),
                "du": du, "incons": incons,
                "cliente": _get(row, "Cliente"), "num_proc": _get(row, "Número do processo"),
            })
            continue

        if excluido_manual:
            stats["nao_importados"] += 1
            continue

        # dedup: Id + Conclusão + Tipo + Responsável (seção 3)
        key = f"{id_}|{conclusao.isoformat()}|{tipo}|{resp}"
        if key in seen:
            stats["duplicatas"] += 1
            continue
        seen.add(key)

        resp_disp = resp or "(Sem responsável)"
        coord_raw = RESP_TO_COORD.get(resp, coord_overrides.get(resp, SEM_COORD))
        if coord_raw == SEM_COORD and resp:
            sem_coord_map[resp] = sem_coord_map.get(resp, 0) + 1
        coord_display = COORD_DISPLAY.get(coord_raw, coord_raw)

        incons = check_incons(tipo, desc, conclusao, fatal, aud)

        cliente = _get(row, "Cliente")
        num_proc = _get(row, "Número do processo")      # seção 16

        registros.append({
            "id": id_, "processo": processo, "tipo": tipo, "desc": desc[:300],
            "status": _get(row, "Status"), "resp": resp_disp,
            "coord": coord_raw, "coord_display": coord_display,
            "conclusao": conclusao.strftime("%d/%m/%Y"), "conclusao_iso": conclusao.isoformat(),
            "du": du, "incons": incons,
            "cliente": cliente, "num_proc": num_proc,
        })
    registros.sort(key=lambda r: (r["conclusao_iso"], r["resp"], r["processo"]))
    registros_futuros.sort(key=lambda r: (r["conclusao_iso"], r["resp"], r["processo"]))
    return registros, sem_coord_map, stats, registros_futuros


# ════════════════════════════════════════════════════════════════════════════
# PERSISTÊNCIA / PUBLICAÇÃO
# ════════════════════════════════════════════════════════════════════════════
def load_published():
    if os.path.exists(DATA_FILE):
        try:
            with open(DATA_FILE, encoding="utf-8") as f:
                data = json.load(f)
                # registros_futuros pode não existir em publicações anteriores a
                # esta versão (seção 19) — sem quebrar a leitura de dados antigos.
                data.setdefault("registros_futuros", [])
                return data
        except Exception:
            pass
    return {"registros": [], "registros_futuros": [], "publicado_em": None, "total": 0,
            "versao": None, "referencia": None}


def save_published(registros, versao, today_str, registros_futuros=None):
    data = {"registros": registros, "registros_futuros": registros_futuros or [],
            "publicado_em": datetime.now().strftime("%d/%m/%Y %H:%M"),
            "total": len(registros), "versao": versao, "referencia": today_str}
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, default=str)
    return data


def clear_published():
    """Apaga somente os registros importados/publicados (DATA_FILE). Não mexe em
    COORD_MAP, EXCLUDED_SET nem em nenhuma outra configuração do sistema."""
    if os.path.exists(DATA_FILE):
        os.remove(DATA_FILE)


def learn_coord_overrides(coord_overrides):
    """Grava permanentemente os vínculos responsável→coordenador escolhidos
    manualmente na carga (seção 8), para que as próximas importações já
    reconheçam esses responsáveis automaticamente."""
    if not coord_overrides:
        return
    aprendidos = {}
    if os.path.exists(LEARNED_COORD_FILE):
        try:
            with open(LEARNED_COORD_FILE, encoding="utf-8") as f:
                aprendidos = json.load(f)
        except Exception:
            aprendidos = {}
    aprendidos.update(coord_overrides)
    with open(LEARNED_COORD_FILE, "w", encoding="utf-8") as f:
        json.dump(aprendidos, f, ensure_ascii=False, indent=2)


def learn_resp_corrections(resp_corrections):
    """Grava permanentemente as correções de nome de responsável (seção 8),
    para que as próximas cargas já reconheçam o nome corrigido."""
    if not resp_corrections:
        return
    aprendidos = {}
    if os.path.exists(LEARNED_NAME_FILE):
        try:
            with open(LEARNED_NAME_FILE, encoding="utf-8") as f:
                aprendidos = json.load(f)
        except Exception:
            aprendidos = {}
    aprendidos.update(resp_corrections)
    with open(LEARNED_NAME_FILE, "w", encoding="utf-8") as f:
        json.dump(aprendidos, f, ensure_ascii=False, indent=2)


def learn_resp_excluir(resp_excluir):
    """Grava permanentemente os responsáveis marcados para nunca importar
    (seção 8), para que as próximas cargas já os descartem automaticamente."""
    if not resp_excluir:
        return
    excluidos = set()
    if os.path.exists(LEARNED_EXCLUDE_FILE):
        try:
            with open(LEARNED_EXCLUDE_FILE, encoding="utf-8") as f:
                excluidos = set(json.load(f))
        except Exception:
            excluidos = set()
    excluidos |= set(resp_excluir)
    with open(LEARNED_EXCLUDE_FILE, "w", encoding="utf-8") as f:
        json.dump(sorted(excluidos), f, ensure_ascii=False, indent=2)


def push_to_github(token, repo_name, file_path, content, commit_msg):
    try:
        from github import Github
        g = Github(token)
        repo = g.get_repo(repo_name)
        try:
            existing = repo.get_contents(file_path)
            repo.update_file(file_path, commit_msg, content, existing.sha)
        except Exception:
            repo.create_file(file_path, commit_msg, content)
        return True, None
    except Exception as e:
        return False, str(e)


def delete_from_github(token, repo_name, file_path, commit_msg):
    """Remove o arquivo publicado também no GitHub (usado pelo Limpar Base).
    Sem isso, uma limpeza feita só localmente é desfeita assim que o app
    reinicia/reimplanta, pois o container volta a clonar a última versão
    commitada do repositório (seção 'Manutenção da base')."""
    try:
        from github import Github
        g = Github(token)
        repo = g.get_repo(repo_name)
        existing = repo.get_contents(file_path)
        repo.delete_file(file_path, commit_msg, existing.sha)
        return True, None
    except Exception as e:
        return False, str(e)


# ════════════════════════════════════════════════════════════════════════════
# EXPORTAÇÃO EXCEL / CSV (seção 13)
# ════════════════════════════════════════════════════════════════════════════
COLS_DETAIL = ["Processo", "Cliente", "Número do Processo", "Tipo", "Descrição",
               "Coordenador", "Responsável", "Conclusão Prevista"]
# Auditoria (única aba que ainda exibe inconsistências) usa esta variante.
COLS_DETAIL_AUDITORIA = COLS_DETAIL + ["Inconsistência"]
COLS_RESUMO = ["Responsável", "Prazo", "Audiência", "Diversos", "Pauta de Julgamento",
               "Perícia", "Publicação", "Total"]


def _hstyle(cell):
    cell.fill = PatternFill("solid", fgColor=CLR_HEADER)
    cell.font = Font(bold=True, color=CLR_HEADER_TXT, size=10)
    cell.alignment = Alignment(horizontal="center", vertical="center", wrap_text=True)


def apply_row_style(ws, row_num, du, tipo, num_cols):
    bg, txt = get_row_color(du, tipo)
    if not bg:
        return
    fill = PatternFill("solid", fgColor=bg)
    font = Font(color=txt, size=10)
    for col in range(1, num_cols + 1):
        ws.cell(row=row_num, column=col).fill = fill
        ws.cell(row=row_num, column=col).font = font


def write_sheet(ws, data_rows, cols, is_resumo=False):
    ws.row_dimensions[1].height = 30
    for ci, col in enumerate(cols, 1):
        _hstyle(ws.cell(row=1, column=ci, value=col))
    for ri, row in enumerate(data_rows, 2):
        for ci, col in enumerate(cols, 1):
            cell = ws.cell(row=ri, column=ci, value=row.get(col, ""))
            cell.alignment = Alignment(vertical="top", wrap_text=(cols[ci - 1] == "Descrição"))
            cell.font = Font(size=10)
        if not is_resumo:
            apply_row_style(ws, ri, row.get("Dias Úteis"), row.get("Tipo", ""), len(cols))
        elif row.get("Responsável") == "TOTAL":
            for ci in range(1, len(cols) + 1):
                ws.cell(row=ri, column=ci).fill = PatternFill("solid", fgColor=CLR_GOLD)
                ws.cell(row=ri, column=ci).font = Font(bold=True, color=CLR_GOLD_TXT, size=10)
    for ci, col in enumerate(cols, 1):
        max_len = max([len(str(col))] + [len(str(r.get(col, ""))) for r in data_rows[:50]] or [8])
        ws.column_dimensions[get_column_letter(ci)].width = min(max(max_len + 2, 8), 50)
    ws.freeze_panes = "A2"
    if ws.max_row >= 1:
        ws.auto_filter.ref = ws.dimensions


def _to_detail(r):
    return {"Processo": r["processo"], "Cliente": r.get("cliente", ""),
            "Número do Processo": r.get("num_proc", ""), "Tipo": r["tipo"], "Descrição": r["desc"],
            "Coordenador": r["coord_display"], "Responsável": r["resp"],
            "Conclusão Prevista": r["conclusao"], "Inconsistência": r["incons"],
            "Dias Úteis": r["du"]}


def gerar_excel_coord(coord_key, registros, coord_display):
    rows = [r for r in registros if r["coord"] == coord_key and r["resp"] not in EXCLUDED_SET]
    rows.sort(key=lambda r: (r["conclusao_iso"], r["resp"], r["processo"]))
    wb = openpyxl.Workbook()

    by_resp = {}
    for r in rows:
        rp = r["resp"]
        o = by_resp.setdefault(rp, {"Responsável": rp, "Prazo": 0, "Audiência": 0, "Diversos": 0,
                                    "Pauta de Julgamento": 0, "Perícia": 0, "Publicação": 0,
                                    "Total": 0})
        t = r["tipo"]
        if t in ("Prazo", "Audiência", "Pauta de Julgamento", "Perícia", "Publicação"):
            o[t] += 1
        else:
            o["Diversos"] += 1
        o["Total"] += 1
    resumo_rows = sorted(by_resp.values(), key=lambda x: -x["Total"])
    tot = {c: sum(r.get(c, 0) for r in resumo_rows if isinstance(r.get(c, 0), int)) for c in COLS_RESUMO[1:]}
    tot["Responsável"] = "TOTAL"
    resumo_rows.append(tot)

    ws_res = wb.active
    ws_res.title = "Resumo"
    write_sheet(ws_res, resumo_rows, COLS_RESUMO, is_resumo=True)

    for tipo_key, nome_aba in [("Prazo", "Prazos"), ("Audiência", "Audiências"), ("Diversos", "Diversos")]:
        write_sheet(wb.create_sheet(nome_aba), [_to_detail(r) for r in rows if r["tipo"] == tipo_key], COLS_DETAIL)

    buf = io.BytesIO()
    wb.save(buf)
    buf.seek(0)
    return buf


def exportar_xlsx_filtrado(rows, cols=COLS_DETAIL):
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Dados"
    write_sheet(ws, [_to_detail(r) for r in rows], cols)
    buf = io.BytesIO()
    wb.save(buf)
    buf.seek(0)
    return buf


# ════════════════════════════════════════════════════════════════════════════
# CAMADA VISUAL — CSS + componentes (design system vinho/dourado)
# ════════════════════════════════════════════════════════════════════════════
def _logo_b64():
    base = os.path.dirname(os.path.abspath(globals().get("__file__", "app.py")))
    for p in ["project/assets/logo-igsa.jpg", "assets/logo-igsa.jpg",
              os.path.join(base, "project/assets/logo-igsa.jpg")]:
        if os.path.exists(p):
            with open(p, "rb") as f:
                return base64.b64encode(f.read()).decode()
    return ""


LOGO_B64 = _logo_b64()


def inject_css():
    st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cinzel:wght@500;600&family=Cormorant+Garamond:wght@500;600;700&family=Libre+Franklin:wght@300;400;500;600;700&family=IBM+Plex+Mono:wght@400;500&display=swap');
    :root{--wine:#7E1F2D;--wine-d:#641828;--wine-l:#9B2335;--gold:#CDA736;--gold-d:#8E6E1C;
          --ink:#2A2420;--muted:#756A5D;--sand:#F7F2E9;--border:#E5DAC7;--green:#2E9E5B;}
    html,body,[class*="css"],.stMarkdown{font-family:'Libre Franklin',sans-serif;color:var(--ink)}
    .stApp{background:#F7F2E9}
    .block-container{padding-top:1.6rem;max-width:1200px}
    /* Sidebar vinho */
    section[data-testid="stSidebar"]{background:linear-gradient(160deg,#651823 0%,#7E1F2D 55%,#9E3340 100%)}
    section[data-testid="stSidebar"] *{color:#F5E9C2}
    section[data-testid="stSidebar"] .stButton>button{
        width:100%;text-align:left;background:rgba(255,255,255,.03);color:#EbD9C6;border:1px solid rgba(205,167,54,.15);
        border-radius:8px;padding:.55rem .8rem;font-size:13.5px;font-weight:500;margin-bottom:2px;transition:all .15s}
    section[data-testid="stSidebar"] .stButton>button:hover{background:rgba(255,255,255,.09);border-color:rgba(205,167,54,.4)}
    section[data-testid="stSidebar"] .stButton>button:focus{box-shadow:none;color:#fff}
    section[data-testid="stSidebar"] .stButton>button[kind="primary"]{background:var(--wine-d)!important;color:#fff!important;
        border-left:3px solid var(--gold)!important;font-weight:600!important}
    /* Header */
    .ig-kicker{font-size:11px;letter-spacing:.14em;text-transform:uppercase;color:var(--gold-d);font-weight:600;margin-bottom:6px}
    .ig-title{font-family:'Cormorant Garamond',serif;font-size:40px;font-weight:600;color:var(--ink);line-height:1.1;margin:0}
    .ig-ref{display:inline-flex;align-items:center;gap:7px;color:var(--gold-d);font-weight:600;font-size:13px;margin-top:8px}
    /* Cards */
    .ig-card{position:relative;background:#fff;border:1px solid var(--border);border-radius:12px;
        padding:15px 16px;box-shadow:0 1px 3px rgba(56,11,17,.07);overflow:hidden;margin-bottom:6px}
    .ig-card::before{content:'';position:absolute;top:0;left:0;right:0;height:3px;background:var(--acc,#7E1F2D)}
    .ig-card .k{font-size:9.5px;letter-spacing:.09em;text-transform:uppercase;color:var(--gold-d);font-weight:700;margin-bottom:6px}
    .ig-card .v{font-family:'Cormorant Garamond',serif;font-size:30px;font-weight:600;color:var(--ink);line-height:1}
    .ig-tile{border-radius:12px;padding:18px 20px;box-shadow:0 1px 3px rgba(56,11,17,.07)}
    .ig-tile .tl{font-size:12px;font-weight:700;letter-spacing:.04em;text-transform:uppercase}
    .ig-tile .tv{font-family:'Cormorant Garamond',serif;font-size:44px;font-weight:600;line-height:1.05;margin:6px 0 2px}
    .ig-tile .td{font-size:12px;opacity:.82}
    .ig-sec{font-size:11px;letter-spacing:.09em;text-transform:uppercase;color:var(--wine);font-weight:600;
        border-bottom:1px solid var(--border);padding-bottom:7px;margin:22px 0 12px}
    /* Tabelas HTML */
    .ig-tw{max-height:var(--h,440px);overflow:auto;border:1px solid var(--border);border-radius:10px;background:#fff}
    .ig-tw table{width:100%;border-collapse:collapse;font-size:12px}
    .ig-tw thead th{background:var(--wine);color:#fff;padding:8px 10px;text-align:left;font-size:10px;
        letter-spacing:.04em;text-transform:uppercase;font-weight:600;position:sticky;top:0;white-space:nowrap}
    .ig-tw tbody td{padding:6px 10px;border-bottom:1px solid #EDE5D4;vertical-align:top}
    .ig-tw tbody tr:hover td{filter:brightness(.97)}
    .ig-legend{background:#fff;border:1px solid var(--border);border-radius:8px;padding:9px 14px;margin:6px 0 12px;
        display:flex;flex-wrap:wrap;gap:12px 16px;align-items:center;font-size:11px}
    .ig-legend b{color:var(--wine);letter-spacing:.05em;font-size:10px}
    .ig-legend span.sw{width:13px;height:13px;border-radius:3px;display:inline-block;border:1px solid rgba(0,0,0,.08);vertical-align:middle;margin-right:5px}
    .ig-pub{background:rgba(0,0,0,.16);border:1px solid rgba(205,167,54,.22);border-radius:10px;padding:12px 14px;
        font-size:11.5px;line-height:1.55}
    .ig-pub .dot{width:7px;height:7px;border-radius:50%;background:#43B26C;display:inline-block;margin-right:6px}
    /* Botão dourado (Controladoria) */
    div[data-testid="stButton"] .accent>button{background:var(--gold);color:#4E121A;text-transform:uppercase;
        letter-spacing:.08em;font-weight:600;border:none}
    </style>
    """, unsafe_allow_html=True)


def render_header(kicker, title, ref=None, sub=None):
    cal = ('<svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" '
           'stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round"><rect x="3" y="4" '
           'width="18" height="18" rx="2"></rect><line x1="16" y1="2" x2="16" y2="6"></line>'
           '<line x1="8" y1="2" x2="8" y2="6"></line><line x1="3" y1="10" x2="21" y2="10"></line></svg>')
    ref_html = f'<div class="ig-ref">{cal} Referência {ref}</div>' if ref else \
               (f'<div style="margin-top:8px;font-size:13px;color:var(--muted)">{sub}</div>' if sub else "")
    st.markdown(
        f'<div class="ig-kicker">{kicker}</div><h1 class="ig-title">{title}</h1>{ref_html}',
        unsafe_allow_html=True)


def card(kicker, value, accent="#7E1F2D"):
    return f'<div class="ig-card" style="--acc:{accent}"><div class="k">{kicker}</div><div class="v">{value}</div></div>'


def cards_row(items, ncols):
    cols = st.columns(ncols)
    for i, (k, v, acc) in enumerate(items):
        with cols[i % ncols]:
            st.markdown(card(k, v, acc), unsafe_allow_html=True)


def render_color_legend():
    st.markdown(
        '<div class="ig-legend"><b>LEGENDA</b>'
        '<span><span class="sw" style="background:#C6EFCE"></span>No prazo</span>'
        '<span><span class="sw" style="background:#FFEB9C"></span>Amanhã (D-1)</span>'
        '<span><span class="sw" style="background:#FFC7CE"></span>Vence hoje</span>'
        '<span><span class="sw" style="background:#FFDDB3"></span>Vencido / pendente</span></div>',
        unsafe_allow_html=True)


def render_html_table(df, height=440, color_rows=True):
    if df is None or df.empty:
        st.info("Nenhum registro para os filtros selecionados.")
        return
    visible = [c for c in df.columns if not c.startswith("_")]
    thead = "".join(f"<th>{c}</th>" for c in visible)
    body = []
    for _, row in df.iterrows():
        bg, fg = "", ""
        if color_rows:
            bg, fg = get_row_color(row.get("_du"), str(row.get("Tipo", "") or ""))
        style = f'style="background:#{bg};color:#{fg}"' if bg else ""
        tds = "".join(f"<td>{'' if pd.isna(v) else v}</td>" for c, v in zip(df.columns, row.tolist()) if not c.startswith("_"))
        body.append(f"<tr {style}>{tds}</tr>")
    st.markdown(
        f'<div class="ig-tw" style="--h:{height}px"><table><thead><tr>{thead}</tr></thead>'
        f'<tbody>{"".join(body)}</tbody></table></div>', unsafe_allow_html=True)


# ---- Gráficos (Altair) ----
def chart_bar_h(df_data, val_col, lbl_col, color="#7E1F2D", height=None):
    if df_data.empty:
        return
    import altair as alt
    d = df_data.copy()
    d["_f"] = d[val_col].apply(fmt_num)
    base = alt.Chart(d).encode(
        y=alt.Y(f"{lbl_col}:N", sort="-x", title=None, axis=alt.Axis(labelLimit=200, labelFontSize=11)),
        x=alt.X(f"{val_col}:Q", title=None, axis=alt.Axis(labels=False, ticks=False),
                scale=alt.Scale(domain=[0, float(d[val_col].max()) * 1.18])))
    bars = base.mark_bar(color=color, cornerRadiusTopRight=4, cornerRadiusBottomRight=4)
    labels = base.mark_text(align="left", dx=5, fontSize=12, fontWeight="bold", color="#2A2420").encode(text="_f:N")
    # height fixo (ex.: para pareamento simétrico com outro gráfico) ou proporcional
    # à quantidade de linhas, para não distorcer com poucos itens.
    st.altair_chart((bars + labels).properties(height=height or max(200, 26 * len(d)))
                    .configure_axis(grid=True, gridColor="#EDE5D4").configure_view(strokeWidth=0),
                    use_container_width=True)


def chart_donut(labels, values):
    if not values or sum(values) == 0:
        return
    import altair as alt
    d = pd.DataFrame({"Tipo": labels, "Qtd": values})
    total = sum(values)
    d["_pct"] = (d["Qtd"] / total * 100).round(1)
    base = alt.Chart(d).encode(
        theta=alt.Theta("Qtd:Q", stack=True),
        color=alt.Color("Tipo:N", scale=alt.Scale(range=MULTI_COLORS),
                        legend=alt.Legend(orient="right", title=None, labelFontSize=11)),
        tooltip=["Tipo", alt.Tooltip("Qtd", format=","), alt.Tooltip("_pct", title="%")])
    pie = base.mark_arc(innerRadius=55, outerRadius=95)
    center = alt.Chart(pd.DataFrame({"t": [f"{fmt_num(total)}"]})).mark_text(
        size=22, fontWeight="bold", color="#2A2420", font="Cormorant Garamond").encode(text="t:N")
    st.altair_chart((pie + center).properties(height=260).configure_view(strokeWidth=0), use_container_width=True)


# ---- Tabela "Prazos por responsável" (seção 14) ----
def _agg_prazos_por_responsavel(active_df, tipo_filter):
    """Agrega prazos (SOMENTE tipo Prazo) por responsável, com totais por status (manual §14)."""
    if tipo_filter not in ("Todos", "Prazo"):
        return None
    prazos = active_df[active_df["tipo"] == "Prazo"]
    if prazos.empty:
        return None
    agg = {}
    for _, r in prazos.iterrows():
        k = r["resp"]
        o = agg.setdefault(k, {"resp": k, "coord": r["coord_display"], "total": 0,
                               "d1": 0, "fatal": 0, "venc": 0, "dentro": 0})
        o["total"] += 1
        du = r["du"]
        if du == 1:
            o["d1"] += 1
        elif du == 0:
            o["fatal"] += 1
        elif du < 0:
            o["venc"] += 1
        else:
            o["dentro"] += 1
    return list(agg.values())


def _tabela_prazos_por_responsavel_html(linhas, height=480):
    def cell(v, bg):
        return f'<td style="text-align:center;font-weight:600;background:{bg}">{v or ""}</td>' if v else \
               '<td style="text-align:center"></td>'

    head = ("<tr><th>Responsável</th><th>Coordenador</th>"
            "<th style='text-align:center;background:#641828'>Total</th>"
            "<th style='text-align:center'>D-1</th><th style='text-align:center'>Fatal</th>"
            "<th style='text-align:center'>Vencido</th><th style='text-align:center'>No prazo</th>"
            "<th style='text-align:center;background:#DEC158;color:#4E121A'>Em atraso</th></tr>")
    rows_html = []
    tg = {"total": 0, "d1": 0, "fatal": 0, "venc": 0, "dentro": 0}
    for o in linhas:
        for kk in tg:
            tg[kk] += o[kk]
        atraso = o["fatal"] + o["venc"]
        rows_html.append(
            "<tr>"
            f'<td style="font-weight:500">{abbrev_name(o["resp"])}</td>'
            f'<td style="color:#756A5D;font-size:11.5px">{abbrev_name(o["coord"])}</td>'
            f'<td style="text-align:center;font-weight:700;color:#651823">{o["total"]}</td>'
            + cell(o["d1"], "#FFEB9C") + cell(o["fatal"], "#FFC7CE")
            + cell(o["venc"], "#FFDDB3")
            + cell(o["dentro"], "#C6EFCE")
            + (f'<td style="text-align:center;font-weight:700;background:#F6DBDD;color:#651823">{atraso}</td>' if atraso else '<td style="text-align:center"></td>')
            + "</tr>")
    atraso_tg = tg["fatal"] + tg["venc"]
    rows_html.append(
        '<tr style="border-top:2px solid #7E1F2D;background:#F7F2E9;font-weight:700">'
        '<td colspan="2">TOTAL GERAL</td>'
        f'<td style="text-align:center;color:#651823">{tg["total"]}</td>'
        f'<td style="text-align:center">{tg["d1"] or ""}</td><td style="text-align:center">{tg["fatal"] or ""}</td>'
        f'<td style="text-align:center">{tg["venc"] or ""}</td><td style="text-align:center">{tg["dentro"] or ""}</td>'
        f'<td style="text-align:center">{atraso_tg or ""}</td></tr>')
    st.markdown(
        f'<div class="ig-tw" style="--h:{height}px"><table><thead>{head}</thead>'
        f'<tbody>{"".join(rows_html)}</tbody></table></div>', unsafe_allow_html=True)


def _tabela_prazos_por_coordenador_html(linhas, height=480):
    def cell(v, bg):
        return f'<td style="text-align:center;font-weight:600;background:{bg}">{v or ""}</td>' if v else \
               '<td style="text-align:center"></td>'

    head = ("<tr><th>Coordenador</th>"
            "<th style='text-align:center;background:#641828'>Total</th>"
            "<th style='text-align:center'>D-1</th><th style='text-align:center'>Fatal</th>"
            "<th style='text-align:center'>Vencido</th><th style='text-align:center'>No prazo</th>"
            "<th style='text-align:center;background:#DEC158;color:#4E121A'>Em atraso</th></tr>")
    rows_html = []
    tg = {"total": 0, "d1": 0, "fatal": 0, "venc": 0, "dentro": 0}
    for o in linhas:
        for kk in tg:
            tg[kk] += o[kk]
        atraso = o["fatal"] + o["venc"]
        rows_html.append(
            "<tr>"
            f'<td style="font-weight:500">{abbrev_name(o["coord"])}</td>'
            f'<td style="text-align:center;font-weight:700;color:#651823">{o["total"]}</td>'
            + cell(o["d1"], "#FFEB9C") + cell(o["fatal"], "#FFC7CE")
            + cell(o["venc"], "#FFDDB3")
            + cell(o["dentro"], "#C6EFCE")
            + (f'<td style="text-align:center;font-weight:700;background:#F6DBDD;color:#651823">{atraso}</td>' if atraso else '<td style="text-align:center"></td>')
            + "</tr>")
    atraso_tg = tg["fatal"] + tg["venc"]
    rows_html.append(
        '<tr style="border-top:2px solid #7E1F2D;background:#F7F2E9;font-weight:700">'
        '<td>TOTAL GERAL</td>'
        f'<td style="text-align:center;color:#651823">{tg["total"]}</td>'
        f'<td style="text-align:center">{tg["d1"] or ""}</td><td style="text-align:center">{tg["fatal"] or ""}</td>'
        f'<td style="text-align:center">{tg["venc"] or ""}</td><td style="text-align:center">{tg["dentro"] or ""}</td>'
        f'<td style="text-align:center">{atraso_tg or ""}</td></tr>')
    st.markdown(
        f'<div class="ig-tw" style="--h:{height}px"><table><thead>{head}</thead>'
        f'<tbody>{"".join(rows_html)}</tbody></table></div>', unsafe_allow_html=True)


def render_tabelas_prazos(active_df, tipo_filter):
    """Duas tabelas empilhadas, largura total e mesmo padrão visual: Prazos por
    Coordenador (Tabela 1, acima) e Prazos por Responsável (Tabela 2, abaixo,
    ordenada por coordenador, responsáveis preservados dentro de cada um)."""
    HEIGHT = 480
    agg = _agg_prazos_por_responsavel(active_df, tipo_filter)

    st.markdown('<div class="ig-sec">Prazos por coordenador</div>', unsafe_allow_html=True)
    st.caption("Total de prazos de cada coordenador, com a situação por status.")
    if agg is None:
        st.info("Nenhum prazo encontrado.")
    else:
        by_coord = {}
        for o in agg:
            c = by_coord.setdefault(o["coord"], {"coord": o["coord"], "total": 0,
                                                  "d1": 0, "fatal": 0, "venc": 0, "dentro": 0})
            for kk in ("total", "d1", "fatal", "venc", "dentro"):
                c[kk] += o[kk]
        linhas_c = sorted(by_coord.values(), key=lambda x: abbrev_name(x["coord"]).lower())
        _tabela_prazos_por_coordenador_html(linhas_c, height=HEIGHT)

    st.markdown('<div class="ig-sec">Prazos por responsável</div>', unsafe_allow_html=True)
    st.caption("Responsável e seu Coordenador, com a situação dos prazos por status.")
    if agg is None:
        st.info("Nenhum prazo encontrado.")
    else:
        linhas_r = sorted(agg, key=lambda x: (abbrev_name(x["coord"]).lower(), abbrev_name(x["resp"]).lower()))
        _tabela_prazos_por_responsavel_html(linhas_r, height=HEIGHT)


# ════════════════════════════════════════════════════════════════════════════
# FILTROS COMPARTILHADOS
# ════════════════════════════════════════════════════════════════════════════
def base_df(registros):
    """DataFrame público: sem coordenações ocultas, sem responsável vazio/ausente.
    Prazos sem responsável ficam de fora de toda tela/gráfico/indicador (mas
    continuam armazenados em dados_publicados.json)."""
    if not registros:
        return pd.DataFrame()
    df = pd.DataFrame(registros)
    df["conclusao_dt"] = pd.to_datetime(df["conclusao_iso"])
    df = df[df["resp"].notna() & (df["resp"] != "") & (df["resp"] != "nan") &
            (df["resp"] != "(Sem responsável)")]
    df = df[~df["coord"].isin(HIDDEN_COORDS)]                       # seção 11
    return df


def public_df(registros):
    """Recorte público: exclui EXCLUDED_SET (§10). Coordenações ocultas já saem em base_df (§11)."""
    df = base_df(registros)
    if df.empty:
        return df
    return df[~df["resp"].isin(EXCLUDED_SET)]                       # seção 10


def apply_dates(df, ini, fim):
    if ini:
        df = df[df["conclusao_dt"] >= pd.Timestamp(ini)]
    if fim:
        df = df[df["conclusao_dt"] <= pd.Timestamp(fim)]
    return df


# Legenda/situação do prazo — mesma lógica de "du" usada nos indicadores
# e nas tabelas Prazos por Coordenador/Responsável (seção 14).
STATUS_OPCOES = ["No prazo", "Amanhã (D-1)", "Vence hoje", "Vencido / Pendente"]


def apply_status(df, status_f):
    if not status_f or set(status_f) == set(STATUS_OPCOES):
        return df
    cond = pd.Series(False, index=df.index)
    if "No prazo" in status_f:
        cond |= df["du"] > 1
    if "Amanhã (D-1)" in status_f:
        cond |= df["du"] == 1
    if "Vence hoje" in status_f:
        cond |= df["du"] == 0
    if "Vencido / Pendente" in status_f:
        cond |= df["du"] < 0
    return df[cond]


# ════════════════════════════════════════════════════════════════════════════
# PÁGINAS
# ════════════════════════════════════════════════════════════════════════════
def metric_items(df):
    def c(t):
        return fmt_num(len(df[df.tipo == t]))
    return [("Total", fmt_num(len(df)), WINE), ("Prazos", c("Prazo"), "#9E3340"),
            ("Audiências", c("Audiência"), GOLD), ("Diversos", c("Diversos"), GOLD_DARK),
            ("Pauta Julg.", c("Pauta de Julgamento"), GREEN), ("Perícia", c("Perícia"), "#BE5862"),
            ("Publicação", c("Publicação"), "#651823")]


def page_geral(registros, ref):
    render_header("Portal de Gestão de Prazos", "Visão Geral", ref=ref)
    df0 = public_df(registros)
    if df0.empty:
        st.info("Nenhum dado disponível. Publique uma planilha na Área Administrativa.")
        return

    c1, c2, c3, c4, c5, c6 = st.columns(6)
    ini = c1.date_input("Data Início", value=None, key="g_ini")
    fim = c2.date_input("Data Fim", value=None, key="g_fim")
    coords = sorted(df0["coord_display"].dropna().unique().tolist())
    coord_f = c3.multiselect("Coordenador", coords, key="g_coord")
    resps = sorted(df0["resp"].dropna().unique().tolist())
    resp_f = c4.multiselect("Responsável", resps, key="g_resp")
    tipos = ["Todos"] + [t for t in TIPOS_CONHECIDOS if t in df0["tipo"].unique()]
    tipo_f = c5.selectbox("Tipo", tipos, key="g_tipo")
    proc_f = c6.text_input("Buscar processo / cliente", key="g_proc")

    layout = st.radio("Layout", ["Panorama", "Prioridades"], horizontal=True, key="g_layout")

    # Filtro único: vale para Panorama/Prioridades E para as tabelas Prazos por
    # Coordenador/Responsável ao final da página — nada fica fora do filtro.
    # Coordenador/Responsável vazios = sem filtro (todos).
    df = apply_dates(df0, ini, fim)
    if coord_f:
        df = df[df["coord_display"].isin(coord_f)]
    if resp_f:
        df = df[df["resp"].isin(resp_f)]
    if tipo_f != "Todos":
        df = df[df["tipo"] == tipo_f]
    if proc_f:
        q = proc_f.lower()
        df = df[df["processo"].str.lower().str.contains(q, na=False) |
                df["cliente"].str.lower().str.contains(q, na=False)]

    if layout == "Panorama":
        cards_row(metric_items(df), 7)
        st.markdown('<div class="ig-sec">Composição por tipo · Distribuição por coordenador</div>', unsafe_allow_html=True)
        ca, cb = st.columns(2)
        with ca:
            by_t = df.groupby("tipo").size().reset_index(name="q").sort_values("q", ascending=False)
            chart_donut(by_t["tipo"].tolist(), by_t["q"].tolist())
        with cb:
            by_c = df.groupby("coord_display").size().reset_index(name="Pendências").sort_values("Pendências", ascending=False)
            by_c["coord_display"] = by_c["coord_display"].apply(abbrev_name)
            chart_bar_h(by_c, "Pendências", "coord_display", WINE, height=260)
        st.markdown('<div class="ig-sec">Responsáveis com mais pendências</div>', unsafe_allow_html=True)
        top = (df.groupby("resp").size()
               .reset_index(name="Qtd").sort_values("Qtd", ascending=False).head(10))
        top["resp"] = top["resp"].apply(abbrev_name)
        chart_bar_h(top, "Qtd", "resp", WINE)
    else:  # Prioridades
        s = lambda cond: fmt_num(len(df[cond]))
        tiles = [("Vencidos", s(df.du < 0), "#FFDDB3", "#8A4B12", "pendentes de baixa"),
                 ("Vencem hoje", s(df.du == 0), "#FADFE3", "#8E1220", "prazo fatal"),
                 ("Amanhã (D-1)", s(df.du == 1), "#FAEFC9", "#6b5410", "agir hoje"),
                 ("Total pendente", fmt_num(len(df)), "#F6DBDD", "#651823", "no recorte atual")]
        cols = st.columns(4)
        for i, (lb, v, bg, fg, dsc) in enumerate(tiles):
            cols[i].markdown(f'<div class="ig-tile" style="background:{bg};color:{fg}"><div class="tl">{lb}</div>'
                             f'<div class="tv">{v}</div><div class="td">{dsc}</div></div>', unsafe_allow_html=True)
        st.markdown('<div class="ig-sec">Composição por tipo · Responsáveis com mais pendências</div>', unsafe_allow_html=True)
        ca, cb = st.columns([1, 1.2])
        with ca:
            by_t = df.groupby("tipo").size().reset_index(name="q").sort_values("q", ascending=False)
            chart_donut(by_t["tipo"].tolist(), by_t["q"].tolist())
        with cb:
            top = (df.groupby("resp").size()
                   .reset_index(name="Qtd").sort_values("Qtd", ascending=False).head(10))
            top["resp"] = top["resp"].apply(abbrev_name)
            chart_bar_h(top, "Qtd", "resp", WINE)

    # ---- Prazos por Coordenador / por Responsável (seção 14) ----
    # Usa o mesmo filtro único da página — sem bloco de filtros separado.
    st.markdown('<div class="ig-sec">Prazos por Coordenador e por Responsável</div>', unsafe_allow_html=True)
    render_tabelas_prazos(df, tipo_f)


def page_coordenacao(registros, ref):
    render_header("Controladoria · Equipes", "Por Coordenação",
                  sub="Distribuição e detalhamento das pendências por responsável")
    df0 = public_df(registros)
    if df0.empty:
        st.info("Nenhum dado disponível.")
        return

    c1, c2, c3, c4, c5, c6 = st.columns(6)
    ini = c1.date_input("Data Início", value=None, key="c_ini")
    fim = c2.date_input("Data Fim", value=None, key="c_fim")
    coord_f = c3.multiselect("Coordenador", sorted(df0["coord_display"].dropna().unique().tolist()), key="c_coord")
    resp_f = c4.multiselect("Responsável", sorted(df0["resp"].dropna().unique().tolist()), key="c_resp")
    tipos = ["Todos"] + [t for t in TIPOS_CONHECIDOS if t in df0["tipo"].unique()]
    tipo_f = c5.selectbox("Tipo", tipos, key="c_tipo")
    proc_f = c6.text_input("Buscar processo / cliente", key="c_proc")

    df = apply_dates(df0, ini, fim)
    if coord_f:
        df = df[df["coord_display"].isin(coord_f)]
    if resp_f:
        df = df[df["resp"].isin(resp_f)]
    if tipo_f != "Todos":
        df = df[df["tipo"] == tipo_f]
    if proc_f:
        q = proc_f.lower()
        df = df[df["processo"].str.lower().str.contains(q, na=False) |
                df["cliente"].str.lower().str.contains(q, na=False)]

    cards_row(metric_items(df), 7)

    st.markdown('<div class="ig-sec">Resumo por responsável</div>', unsafe_allow_html=True)
    if df.empty:
        st.info("Nenhum registro para os filtros selecionados.")
    else:
        rr = []
        for resp_name, grp in df.groupby("resp", sort=False):
            known = grp["tipo"].isin(TIPOS_CONHECIDOS)
            rr.append({"Responsável": abbrev_name(resp_name),
                       "Prazo": int((grp.tipo == "Prazo").sum()), "Aud.": int((grp.tipo == "Audiência").sum()),
                       "Pauta": int((grp.tipo == "Pauta de Julgamento").sum()), "Perícia": int((grp.tipo == "Perícia").sum()),
                       "Public.": int((grp.tipo == "Publicação").sum()),
                       "Diversos": int(((grp.tipo == "Diversos") | ~known).sum()),
                       "Total": len(grp)})
        rr.sort(key=lambda x: -x["Total"])
        render_html_table(pd.DataFrame(rr), height=300, color_rows=False)

    st.markdown('<div class="ig-sec">Detalhamento</div>', unsafe_allow_html=True)
    status_f = st.multiselect("Situação do prazo", STATUS_OPCOES, default=STATUS_OPCOES, key="c_status")
    render_color_legend()
    det = apply_status(df, status_f)
    det_view = pd.DataFrame({
        "Processo": det["processo"], "Cliente": det["cliente"], "Tipo": det["tipo"],
        "Descrição": det["desc"], "Coordenador": det["coord_display"].apply(abbrev_name),
        "Responsável": det["resp"].apply(abbrev_name), "Conclusão": det["conclusao"], "_du": det["du"]})
    st.caption(f"Exibindo {min(len(det_view), 200)} de {fmt_num(len(det_view))} registros.")
    render_html_table(det_view.head(200), height=420)

    buf = exportar_xlsx_filtrado(df.to_dict("records"))
    st.download_button("📥 Exportar seleção (Excel)", buf, "IGSA_Filtrado.xlsx",
                       "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")


def page_auditoria(registros, ref):
    render_header("Controladoria · Qualidade", "Auditoria de Inconsistências",
                  sub="Divergências de cadastro a revisar")
    # Auditoria também respeita EXCLUDED_SET (§10) e HIDDEN_COORDS (§11).
    df0 = public_df(registros)
    if df0.empty:
        st.info("Nenhum dado disponível.")
        return
    inc_all = df0[df0["incons"] != ""]

    c1, c2, c3, c4 = st.columns(4)
    ini = c1.date_input("Data Início", value=None, key="a_ini")
    fim = c2.date_input("Data Fim", value=None, key="a_fim")
    coord_f = c3.multiselect("Coordenador", sorted(df0["coord_display"].dropna().unique().tolist()), key="a_coord")
    resp_f = c4.multiselect("Responsável", sorted(df0["resp"].dropna().unique().tolist()), key="a_resp")
    inc_types = sorted({t.strip() for r in inc_all["incons"] for t in r.split(";") if t.strip()})
    ti_f = st.selectbox("Tipo de Inconsistência", ["Todas"] + inc_types, key="a_tipo")

    inc = apply_dates(inc_all, ini, fim)
    if coord_f:
        inc = inc[inc["coord_display"].isin(coord_f)]
    if resp_f:
        inc = inc[inc["resp"].isin(resp_f)]
    if ti_f != "Todas":
        inc = inc[inc["incons"].str.contains(re.escape(ti_f), na=False)]

    st.markdown('<div style="background:linear-gradient(100deg,#FBF6E7,#fff);border:1px solid #EBD58A;'
                'border-radius:10px;padding:12px 16px;margin:6px 0 16px;font-size:13px;color:#4A423B">'
                'Registros com divergência entre tipo, descrição e data de conclusão. '
                'Revise antes de exportar os relatórios das coordenações.</div>', unsafe_allow_html=True)

    types_count = {}
    for r in inc["incons"]:
        for t in r.split(";"):
            t = t.strip()
            if t:
                types_count[t] = types_count.get(t, 0) + 1
    items = [("Total", fmt_num(len(inc)), "#BE5862")] + \
            [(t[:34], fmt_num(v), GOLD) for t, v in sorted(types_count.items(), key=lambda x: -x[1])[:4]]
    cards_row(items, 5)

    st.markdown('<div class="ig-sec">Registros com inconsistência</div>', unsafe_allow_html=True)
    if inc.empty:
        st.markdown('<div style="background:#E2F3E8;border:1px solid #43B26C;border-radius:10px;padding:24px;'
                    'text-align:center;color:#1E6E3E;font-weight:500">Nenhuma inconsistência detectada nos filtros selecionados.</div>',
                    unsafe_allow_html=True)
    else:
        view = pd.DataFrame({
            "Processo": inc["processo"], "Cliente": inc["cliente"], "Tipo": inc["tipo"],
            "Descrição": inc["desc"],
            "Coordenador": inc["coord_display"].apply(abbrev_name), "Responsável": inc["resp"].apply(abbrev_name),
            "Conclusão": inc["conclusao"], "Inconsistência": inc["incons"]})
        # linhas laranja (inconsistência) — cor fixa
        html_rows = "".join(
            "<tr style='background:#F7E3CE;color:#7a4a1f'>" +
            "".join(f"<td>{'' if pd.isna(v) else v}</td>" for v in r) + "</tr>"
            for r in view.itertuples(index=False))
        thead = "".join(f"<th>{c}</th>" for c in view.columns)
        st.markdown(f'<div class="ig-tw" style="--h:460px"><table><thead><tr>{thead}</tr></thead>'
                    f'<tbody>{html_rows}</tbody></table></div>', unsafe_allow_html=True)
        st.download_button("📥 Exportar Inconsistências",
                           exportar_xlsx_filtrado(inc.to_dict("records"), cols=COLS_DETAIL_AUDITORIA),
                           "IGSA_Auditoria.xlsx",
                           "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")


def page_futuros(registros_futuros, ref):
    """Seção 19 · Revisão de Prazos Futuros. Mesmas regras da Auditoria
    (check_incons, EXCLUDED_SET, HIDDEN_COORDS), mas sobre os prazos com
    DU > DU_LIMIT (depois de hoje/D-1) — não interfere em nenhuma outra aba:
    lê de "registros_futuros", uma lista separada de "registros"."""
    render_header("Controladoria · Qualidade", "Revisão de Prazos Futuros",
                  sub="Divergências de cadastro em prazos que ainda não entraram no recorte")
    df0 = public_df(registros_futuros)
    if df0.empty:
        st.info("Nenhum prazo futuro disponível.")
        return
    inc_all = df0[df0["incons"] != ""]

    c1, c2, c3, c4 = st.columns(4)
    ini = c1.date_input("Data Início", value=None, key="f_ini")
    fim = c2.date_input("Data Fim", value=None, key="f_fim")
    coord_f = c3.multiselect("Coordenador", sorted(df0["coord_display"].dropna().unique().tolist()), key="f_coord")
    resp_f = c4.multiselect("Responsável", sorted(df0["resp"].dropna().unique().tolist()), key="f_resp")
    inc_types = sorted({t.strip() for r in inc_all["incons"] for t in r.split(";") if t.strip()})
    ti_f = st.selectbox("Tipo de Inconsistência", ["Todas"] + inc_types, key="f_tipo")

    inc = apply_dates(inc_all, ini, fim)
    if coord_f:
        inc = inc[inc["coord_display"].isin(coord_f)]
    if resp_f:
        inc = inc[inc["resp"].isin(resp_f)]
    if ti_f != "Todas":
        inc = inc[inc["incons"].str.contains(re.escape(ti_f), na=False)]

    st.markdown('<div style="background:linear-gradient(100deg,#FBF6E7,#fff);border:1px solid #EBD58A;'
                'border-radius:10px;padding:12px 16px;margin:6px 0 16px;font-size:13px;color:#4A423B">'
                'Registros com divergência entre tipo, descrição e data de conclusão, entre os prazos com '
                'data além do recorte principal (DU > ' + str(DU_LIMIT) + '). Revise com antecedência, antes '
                'de esses prazos entrarem no painel principal.</div>', unsafe_allow_html=True)

    types_count = {}
    for r in inc["incons"]:
        for t in r.split(";"):
            t = t.strip()
            if t:
                types_count[t] = types_count.get(t, 0) + 1
    items = [("Total", fmt_num(len(inc)), "#BE5862")] + \
            [(t[:34], fmt_num(v), GOLD) for t, v in sorted(types_count.items(), key=lambda x: -x[1])[:4]]
    cards_row(items, 5)

    st.markdown('<div class="ig-sec">Registros com inconsistência</div>', unsafe_allow_html=True)
    if inc.empty:
        st.markdown('<div style="background:#E2F3E8;border:1px solid #43B26C;border-radius:10px;padding:24px;'
                    'text-align:center;color:#1E6E3E;font-weight:500">Nenhuma inconsistência detectada nos filtros selecionados.</div>',
                    unsafe_allow_html=True)
    else:
        view = pd.DataFrame({
            "Processo": inc["processo"], "Cliente": inc["cliente"], "Tipo": inc["tipo"],
            "Descrição": inc["desc"],
            "Coordenador": inc["coord_display"].apply(abbrev_name), "Responsável": inc["resp"].apply(abbrev_name),
            "Conclusão": inc["conclusao"], "Inconsistência": inc["incons"]})
        # linhas laranja (inconsistência) — cor fixa
        html_rows = "".join(
            "<tr style='background:#F7E3CE;color:#7a4a1f'>" +
            "".join(f"<td>{'' if pd.isna(v) else v}</td>" for v in r) + "</tr>"
            for r in view.itertuples(index=False))
        thead = "".join(f"<th>{c}</th>" for c in view.columns)
        st.markdown(f'<div class="ig-tw" style="--h:460px"><table><thead><tr>{thead}</tr></thead>'
                    f'<tbody>{html_rows}</tbody></table></div>', unsafe_allow_html=True)
        st.download_button("📥 Exportar Prazos Futuros",
                           exportar_xlsx_filtrado(inc.to_dict("records"), cols=COLS_DETAIL_AUDITORIA),
                           "IGSA_Prazos_Futuros.xlsx",
                           "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")


def page_exportacao(registros, ref):
    render_header("Controladoria · Relatórios", "Central de Exportação",
                  sub="Gere planilhas por coordenação ou consolidadas")
    if not registros:
        st.info("Nenhum dado disponível.")
        return
    c1, c2 = st.columns(2)
    ini = c1.date_input("Data Início", value=None, key="e_ini")
    fim = c2.date_input("Data Fim", value=None, key="e_fim")

    df = public_df(registros)
    df = apply_dates(df, ini, fim)
    active = df.to_dict("records")
    if not active:
        st.info("Nenhum registro no período selecionado.")
        return

    st.markdown('<div class="ig-sec">Relatório por coordenação</div>', unsafe_allow_html=True)
    st.caption("Cada arquivo traz abas de Resumo, Prazos e Diversos, com formatação condicional por prazo.")
    coords = sorted({r["coord"] for r in active if r["coord"] != SEM_COORD})
    grid = st.columns(3)
    for i, ck in enumerate(coords):
        crows = [r for r in active if r["coord"] == ck]
        disp = COORD_DISPLAY.get(ck, ck)
        n_p = sum(1 for r in crows if r["tipo"] == "Prazo")
        n_a = sum(1 for r in crows if r["tipo"] == "Audiência")
        with grid[i % 3]:
            with st.container(border=True):
                st.markdown(f"**{disp}**")
                st.caption(f"{len(crows)} atividades · {n_p} prazos · {n_a} audiências")
                st.download_button("📥 Baixar Excel", gerar_excel_coord(ck, active, disp),
                                   f"IGSA_{disp[:28].replace(' ', '_')}.xlsx",
                                   "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                                   key=f"dl_{i}")


def page_admin():
    render_header("Controladoria · Restrito", "Área Administrativa", sub="Carga e publicação de dados")
    st.markdown('<div style="background:#FBF6E7;border:1px solid #EBD58A;border-radius:10px;padding:12px 16px;'
                'margin-bottom:16px;font-size:12.5px;color:#8E6E1C"><b>Área restrita.</b> '
                'Uso exclusivo da equipe de Controladoria Jurídica.</div>', unsafe_allow_html=True)

    base_limpa_msg = st.session_state.pop("base_limpa_msg", None)
    if base_limpa_msg:
        st.success(f"{base_limpa_msg} Você já pode importar uma nova planilha.")

    pub = load_published()
    if pub.get("publicado_em"):
        st.markdown(f'<div style="background:linear-gradient(90deg,#1a4731,#2E9E5B);color:#fff;padding:10px 16px;'
                    f'border-radius:8px;margin-bottom:14px;font-size:12px">✓ Publicado em {pub["publicado_em"]} · '
                    f'{fmt_num(pub["total"])} registros · Ref: {pub.get("referencia","—")}</div>', unsafe_allow_html=True)

    st.markdown('<div class="ig-sec">Manutenção da base</div>', unsafe_allow_html=True)
    if not pub.get("publicado_em"):
        st.caption("Nenhum dado publicado no momento.")
    elif st.session_state.get("confirmar_limpeza_base"):
        st.warning(
            f"⚠️ Isso vai excluir **todos os {fmt_num(pub['total'])} registros importados** atualmente publicados. "
            "Coordenadores, usuários e demais configurações do sistema não são afetados. Essa ação não pode ser desfeita.")
        token_salvo = saved_gh_token()
        if token_salvo:
            gh_token_del = token_salvo
            st.caption("🔒 Token do GitHub configurado nos Secrets do app — a limpeza será salva automaticamente.")
        else:
            gh_token_del = st.text_input(
                "GitHub Token (opcional)", type="password", key="gh_token_limpar",
                help="Sem o token, a limpeza só vale para esta sessão do app: se o container reiniciar "
                     "(ex.: o app 'dormir' por inatividade ou uma nova implantação), os dados voltam ao "
                     "último estado salvo no repositório. Preencha para tornar a limpeza definitiva, ou "
                     "configure GITHUB_TOKEN nos Secrets do app para não precisar preencher toda vez.")
        cc1, cc2 = st.columns([1, 1])
        if cc1.button("Confirmar exclusão", type="primary"):
            clear_published()
            msg = "✅ Base local limpa."
            if gh_token_del:
                ok, err = delete_from_github(gh_token_del, GITHUB_REPO, DATA_FILE, "chore: limpar base de prazos")
                msg += " GitHub ✓" if ok else f" ⚠️ GitHub falhou: {err}"
            st.session_state.confirmar_limpeza_base = False
            st.session_state.base_limpa_msg = msg
            st.rerun()
        if cc2.button("Cancelar"):
            st.session_state.confirmar_limpeza_base = False
            st.rerun()
    else:
        if st.button("🗑️ Limpar Base"):
            st.session_state.confirmar_limpeza_base = True
            st.rerun()

    st.markdown('<div class="ig-sec">1 · Carregar planilha</div>', unsafe_allow_html=True)
    today = st.date_input("Data de referência", value=date.today())
    uploaded = st.file_uploader("Selecionar arquivo Excel (exportação LegalOne · .xlsx)", type=["xlsx", "xls"])
    if not uploaded:
        st.info("Formato aceito: exportação LegalOne (.xlsx). O cabeçalho é lido a partir da 2ª linha.")
        return

    with st.spinner("Processando e validando a planilha…"):
        try:
            df, headers = processar_planilha(uploaded)
            faltando = validar_estrutura(headers)
            if faltando:
                st.error(f"❌ Colunas obrigatórias ausentes: {faltando}")
                return
            if len(df) < 5:
                st.error("❌ Arquivo com menos de 5 linhas.")
                return
            registros, sem_coord_map, stats, registros_futuros = construir_registros(df, today)
        except Exception as e:
            st.error(f"❌ Erro ao processar: {e}")
            return
    st.success(f"✅ {fmt_num(len(df))} linhas · {fmt_num(len(registros))} no recorte (DU ≤ {DU_LIMIT})")
    st.caption(
        f"Transparência da carga · {fmt_num(stats['fora_recorte'])} atividades futuras (DU > {DU_LIMIT}) fora do painel "
        f"· {fmt_num(stats['sem_data'])} sem data de conclusão · {fmt_num(stats['duplicatas'])} duplicatas removidas "
        f"· {fmt_num(stats['nao_importados'])} não importados por escolha manual. "
        "Nenhum prazo do recorte é descartado silenciosamente.")
    soma_contas = len(registros) + sum(stats.values())
    st.caption(
        f"Conferência linha a linha: {fmt_num(len(df))} linhas na planilha = {fmt_num(len(registros))} no recorte "
        f"+ {fmt_num(stats['fora_recorte'])} fora do horizonte + {fmt_num(stats['sem_data'])} sem data "
        f"+ {fmt_num(stats['duplicatas'])} duplicatas + {fmt_num(stats['nao_importados'])} não importados "
        f"= {fmt_num(soma_contas)}" + (" ✅ bate certinho." if soma_contas == len(df) else " ⚠️ não bateu — avise a TI."))

    # ---- Seção 8 · Responsáveis sem coordenador — seleção manual na carga ----
    coord_overrides, resp_corrections, resp_excluir = {}, {}, set()
    if sem_coord_map:
        st.markdown('<div class="ig-sec">2 · Responsáveis sem coordenador</div>', unsafe_allow_html=True)
        st.warning(f"{len(sem_coord_map)} responsável(is) sem coordenador mapeado. Para cada um, escolha um "
                   "coordenador, corrija o nome (se for grafia divergente de alguém já cadastrado) ou marque "
                   "para não importar. A escolha é salva automaticamente para as próximas cargas.")
        opcoes = ["(manter sem coordenador)", "🚫 Não importar"] + sorted(COORD_MAP.keys())
        for resp, qtd in sorted(sem_coord_map.items(), key=lambda x: -x[1]):
            cA, cB, cC = st.columns([2, 1.6, 1.6])
            cA.markdown(f"**{resp}** · {qtd} registro(s)")
            nome_corrigido = cB.text_input("Corrigir nome", key=f"nm_{resp}", placeholder="Nome correto (opcional)",
                                           label_visibility="collapsed").strip()
            escolha = cC.selectbox("Coordenador", opcoes, key=f"sc_{resp}", label_visibility="collapsed")
            if escolha == "🚫 Não importar":
                resp_excluir.add(resp)
                continue
            nome_final = resp
            if nome_corrigido and nome_corrigido != resp:
                resp_corrections[resp] = nome_corrigido
                nome_final = nome_corrigido
            if escolha != "(manter sem coordenador)":
                coord_overrides[nome_final] = escolha
        if coord_overrides or resp_corrections or resp_excluir:
            # Grava o aprendizado (vale para esta e para todas as próximas cargas — §8)
            learn_coord_overrides(coord_overrides)
            learn_resp_corrections(resp_corrections)
            learn_resp_excluir(resp_excluir)
            # Reprocessa aplicando as escolhas desta carga
            registros, sem_coord_map, stats, registros_futuros = construir_registros(
                df, today, coord_overrides=coord_overrides,
                resp_corrections=resp_corrections, resp_excluir=resp_excluir)

    # ---- Estatísticas da carga ----
    st.markdown('<div class="ig-sec">Panorama da carga</div>', unsafe_allow_html=True)
    stats = [("Total", fmt_num(len(registros)), WINE),
             ("Prazos", fmt_num(sum(1 for r in registros if r["tipo"] == "Prazo")), "#9E3340"),
             ("Audiências", fmt_num(sum(1 for r in registros if r["tipo"] == "Audiência")), GOLD),
             ("Sem Coord.", fmt_num(sum(1 for r in registros if r["coord"] == SEM_COORD)), "#BE5862")]
    cards_row(stats, 4)

    st.markdown('<div class="ig-sec">Distribuição por coordenação</div>', unsafe_allow_html=True)
    cc = {}
    for r in registros:
        cc[r["coord_display"]] = cc.get(r["coord_display"], 0) + 1
    for k, v in sorted(cc.items(), key=lambda x: -x[1]):
        st.markdown(f'<div style="display:flex;justify-content:space-between;padding:6px 0;'
                    f'border-bottom:1px solid #E5DAC7;font-size:13px"><span>{k}</span>'
                    f'<span style="color:#8E6E1C;font-weight:600">{v}</span></div>', unsafe_allow_html=True)

    # ---- Publicação ----
    st.markdown('<div class="ig-sec">3 · Publicar dados</div>', unsafe_allow_html=True)
    st.caption("Ao publicar, o painel passa a exibir esta carga para toda a equipe.")
    p1, p2 = st.columns([2, 1])
    versao = p1.text_input("Identificação da carga", value=f"{today.strftime('%d/%m/%Y')} — Carga diária (Geral Pendentes)")
    token_salvo = saved_gh_token()
    if token_salvo:
        gh_token = token_salvo
        p2.caption("🔒 Token do GitHub configurado nos Secrets do app — publicação salva automaticamente.")
    else:
        gh_token = p2.text_input("GitHub Token (opcional)", type="password",
                                 help="Sem o token, esta publicação só vale para esta sessão do app: se o "
                                      "container reiniciar (app 'dormir' por inatividade, nova implantação etc.), "
                                      "os dados voltam ao último estado salvo no repositório. Preencha para que "
                                      "esta carga sobreviva a reinícios do app, ou configure GITHUB_TOKEN nos "
                                      "Secrets do app para não precisar preencher toda vez.")
    if st.button("🚀 Publicar no painel", type="primary"):
        with st.spinner("Publicando…"):
            data = save_published(registros, versao, today.strftime("%d/%m/%Y"), registros_futuros)
            msg = f"✅ {fmt_num(len(registros))} registros publicados em {data['publicado_em']}."
            if gh_token:
                with open(DATA_FILE, encoding="utf-8") as f:
                    content = f.read()
                ok, err = push_to_github(gh_token, GITHUB_REPO, DATA_FILE, content, f"chore: publicar dados {versao}")
                msg += " GitHub ✓" if ok else f" ⚠️ GitHub falhou: {err}"
        st.success(msg)
        st.balloons()


# ════════════════════════════════════════════════════════════════════════════
# NAVEGAÇÃO / MAIN
# ════════════════════════════════════════════════════════════════════════════
NAV_ITEMS = [("geral", "Visão Geral"), ("coord", "Por Coordenação"), ("audit", "Auditoria"),
             ("futuros", "Revisão de Prazos Futuros"), ("export", "Exportação"), ("admin", "Área Administrativa")]


def render_sidebar():
    if "page" not in st.session_state:
        st.session_state.page = "geral"
    with st.sidebar:
        if LOGO_B64:
            st.markdown(f'<div style="background:#fff;border-radius:10px;padding:10px;text-align:center;'
                        f'margin-bottom:10px"><img src="data:image/jpeg;base64,{LOGO_B64}" '
                        f'style="width:104px"/></div>', unsafe_allow_html=True)
        st.markdown('<div style="height:1px;background:rgba(205,167,54,.28);margin:8px 4px 14px"></div>',
                    unsafe_allow_html=True)
        for key, label in NAV_ITEMS:
            active = st.session_state.page == key
            if st.button(label, key=f"nav_{key}", use_container_width=True,
                        type="primary" if active else "secondary"):
                st.session_state.page = key
                st.rerun()

        pub = load_published()
        st.markdown('<div style="flex:1;min-height:24px"></div>', unsafe_allow_html=True)
        if pub.get("publicado_em"):
            st.markdown(f'<div class="ig-pub"><div style="color:#EBD58A;font-weight:600;margin-bottom:5px">'
                        f'<span class="dot"></span>Dados publicados</div><div>{pub["publicado_em"]}</div>'
                        f'<div>{fmt_num(pub["total"])} registros · ref. {pub.get("referencia","—")}</div></div>',
                        unsafe_allow_html=True)
        else:
            st.markdown('<div class="ig-pub">● Sem dados publicados</div>', unsafe_allow_html=True)
    return st.session_state.page


def main():
    inject_css()
    page = render_sidebar()
    pub = load_published()
    registros = pub.get("registros", [])
    registros_futuros = pub.get("registros_futuros", [])
    ref = pub.get("referencia") or "01/07/2026"

    if page == "geral":
        page_geral(registros, ref)
    elif page == "coord":
        page_coordenacao(registros, ref)
    elif page == "audit":
        page_auditoria(registros, ref)
    elif page == "futuros":
        page_futuros(registros_futuros, ref)
    elif page == "export":
        page_exportacao(registros, ref)
    elif page == "admin":
        page_admin()


if __name__ == "__main__":
    main()
