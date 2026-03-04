# app_gestao_outside_dashboard.py
# Dashboard Gestão Outside (Streamlit)
# Visual: fundo preto absoluto, cartões premium, detalhes em branco e laranja #FF9400
# Inclui: logo no topo + previsões (pior 1 cliente/mês, melhor 3 clientes/mês)

import os
import streamlit as st
import pandas as pd
from datetime import date, datetime
from dateutil.relativedelta import relativedelta

try:
    import plotly.express as px
except Exception:
    px = None

ACCENT = "#FF9400"
LOGO_PATH = "logogo.jpg"  # coloque seu arquivo de logo com esse nome na mesma pasta do app

st.set_page_config(
    page_title="Gestão Outside | Dashboard",
    page_icon="🟧",
    layout="wide",
)

# =========================
# ESTILO PREMIUM (PRETO + LARANJA)
# =========================
CSS = f"""
<style>
:root {{
  --bg: #000000;
  --panel: #0A0A0D;
  --panel2: #0F0F14;
  --text: #F5F5F7;
  --muted: rgba(245,245,247,0.70);
  --accent: {ACCENT};
  --border: rgba(255,255,255,0.10);
  --glow: rgba(255,148,0,0.20);
}}

html, body, [class*="css"] {{
  background: var(--bg) !important;
  color: var(--text) !important;
}}

div[data-testid="stAppViewContainer"] {{ background: #000000 !important; }}
div[data-testid="stMain"] {{ background: #000000 !important; }}

section[data-testid="stSidebar"] {{
  background: #000000 !important;
  border-right: 1px solid var(--border);
}}

header[data-testid="stHeader"] {{
  background: rgba(0,0,0,0.0) !important;
}}

div[data-testid="stToolbar"] {{
  visibility: hidden;
  height: 0px;
}}

.block-container {{
  padding-top: 1.1rem;
  padding-bottom: 2rem;
  max-width: 1250px;
}}

h1, h2, h3, h4 {{
  color: var(--text) !important;
  letter-spacing: -0.02em;
}}

.hr {{
  height: 1px;
  background: var(--border);
  margin: 18px 0 18px 0;
}}

.badge {{
  display: inline-flex;
  align-items: center;
  gap: 8px;
  padding: 6px 10px;
  border-radius: 999px;
  border: 1px solid var(--border);
  background: rgba(255,255,255,0.03);
  color: var(--muted);
  font-size: 12px;
}}
.badge-dot {{
  width: 7px;
  height: 7px;
  border-radius: 999px;
  background: var(--accent);
  box-shadow: 0 0 18px var(--glow);
}}

.metric-card {{
  background: radial-gradient(1200px 1200px at 10% 0%, rgba(255,148,0,0.08), rgba(0,0,0,0) 38%),
              linear-gradient(180deg, var(--panel) 0%, var(--panel2) 100%);
  border: 1px solid var(--border);
  border-radius: 16px;
  padding: 16px 16px;
  box-shadow: 0 10px 30px rgba(0,0,0,0.55);
}}

.metric-title {{
  color: var(--muted);
  font-size: 12px;
  text-transform: uppercase;
  letter-spacing: 0.08em;
}}

.metric-value {{
  color: var(--text);
  font-size: 34px;
  font-weight: 700;
  margin-top: 6px;
  line-height: 1.2;
}}

.metric-sub {{
  color: var(--muted);
  font-size: 12px;
  margin-top: 6px;
}}

.orange {{
  color: var(--accent);
}}

div[data-testid="stDataFrame"] {{
  background: linear-gradient(180deg, var(--panel) 0%, var(--panel2) 100%);
  border: 1px solid var(--border);
  border-radius: 16px;
  overflow: hidden;
}}

a, a:visited {{
  color: var(--accent) !important;
}}

/* ===== PATCH: inputs sem azul (FOCO / SELECT / UPLOADER / BUTTON) ===== */
*:focus {{ outline: none !important; box-shadow: none !important; }}
*:focus-visible {{ outline: none !important; box-shadow: none !important; }}

div[data-baseweb="select"] > div {{
  background: rgba(255,255,255,0.03) !important;
  border: 1px solid rgba(255,255,255,0.10) !important;
  border-radius: 14px !important;
}}
div[data-baseweb="select"] > div:hover {{
  border-color: {ACCENT} !important;
}}

div[data-testid="stFileUploader"] section {{
  background: rgba(255,255,255,0.03) !important;
  border: 1px solid rgba(255,255,255,0.10) !important;
  border-radius: 16px !important;
}}
div[data-testid="stFileUploader"] section:hover {{
  border-color: {ACCENT} !important;
}}

.stButton > button, button[kind="secondary"], button[kind="primary"] {{
  background: rgba(255,255,255,0.03) !important;
  border: 1px solid rgba(255,255,255,0.10) !important;
  color: #F5F5F7 !important;
  border-radius: 12px !important;
}}
.stButton > button:hover, button[kind="secondary"]:hover, button[kind="primary"]:hover {{
  border-color: {ACCENT} !important;
  color: {ACCENT} !important;
}}

div[data-baseweb="select"] * {{
  box-shadow: none !important;
}}

</style>
"""
st.markdown(CSS, unsafe_allow_html=True)

# =========================
# FUNÇÕES
# =========================
def brl(v: float) -> str:
    if pd.isna(v):
        v = 0.0
    s = f"{float(v):,.2f}"
    s = s.replace(",", "X").replace(".", ",").replace("X", ".")
    return f"R$ {s}"

def safe_lower(x) -> str:
    return str(x).strip().lower()

def month_start(d: date) -> date:
    return date(d.year, d.month, 1)

def add_months(d: date, n: int) -> date:
    return (datetime(d.year, d.month, d.day) + relativedelta(months=n)).date()

def month_label(d: date) -> str:
    return f"{d.month:02d}/{d.year}"

def parse_competencia_to_date(x):
    if pd.isna(x):
        return None

    if isinstance(x, (datetime, date)):
        d = x.date() if isinstance(x, datetime) else x
        return month_start(d)

    s = str(x).strip()

    # tenta YYYY-MM
    try:
        dt = pd.to_datetime(s, format="%Y-%m", errors="raise")
        return date(int(dt.year), int(dt.month), 1)
    except Exception:
        pass

    dt = pd.to_datetime(s, errors="coerce")
    if pd.isna(dt):
        return None
    return date(int(dt.year), int(dt.month), 1)

@st.cache_data(show_spinner=False)
def load_data(file_obj):
    xls = pd.ExcelFile(file_obj)

    clientes = pd.read_excel(xls, "CLIENTES")
    contratos = pd.read_excel(xls, "CONTRATOS")
    faturamento = pd.read_excel(xls, "FATURAMENTO")
    pagamentos = pd.read_excel(xls, "PAGAMENTOS")
    params = pd.read_excel(xls, "PARAMETROS")

    # limpa linhas vazias
    if "cliente_id" in clientes.columns:
        clientes = clientes.dropna(subset=["cliente_id"])
    if "contrato_id" in contratos.columns and "cliente_id" in contratos.columns:
        contratos = contratos.dropna(subset=["contrato_id", "cliente_id"], how="any")
    if "fatura_id" in faturamento.columns and "cliente_id" in faturamento.columns:
        faturamento = faturamento.dropna(subset=["fatura_id", "cliente_id"], how="any")
    if "pagamento_id" in pagamentos.columns and "fatura_id" in pagamentos.columns:
        pagamentos = pagamentos.dropna(subset=["pagamento_id", "fatura_id"], how="any")

    # datas
    if "data_inicio" in contratos.columns:
        contratos["data_inicio"] = pd.to_datetime(contratos["data_inicio"], errors="coerce").dt.date
    if "data_fim" in contratos.columns:
        contratos["data_fim"] = pd.to_datetime(contratos["data_fim"], errors="coerce").dt.date

    if "data_pagamento" in faturamento.columns:
        faturamento["data_pagamento"] = pd.to_datetime(faturamento["data_pagamento"], errors="coerce").dt.date

    if "data_pagamento" in pagamentos.columns:
        pagamentos["data_pagamento"] = pd.to_datetime(pagamentos["data_pagamento"], errors="coerce").dt.date

    # competência
    if "competencia" in faturamento.columns:
        faturamento["competencia_mes"] = faturamento["competencia"].apply(parse_competencia_to_date)
    else:
        faturamento["competencia_mes"] = None

    # numéricos
    faturamento["valor"] = pd.to_numeric(faturamento.get("valor", 0), errors="coerce").fillna(0.0)
    pagamentos["valor_pago"] = pd.to_numeric(pagamentos.get("valor_pago", 0), errors="coerce").fillna(0.0)

    return clientes, contratos, faturamento, pagamentos, params

def compute_received(faturamento_df: pd.DataFrame, pagamentos_df: pd.DataFrame) -> pd.DataFrame:
    fat = faturamento_df.copy()
    pag = pagamentos_df.copy()

    if not pag.empty and "fatura_id" in pag.columns:
        pag_sum = pag.groupby("fatura_id", as_index=False)["valor_pago"].sum()
        fat = fat.merge(pag_sum, on="fatura_id", how="left")
        fat["valor_pago_sum"] = fat["valor_pago"].fillna(0.0)
        fat = fat.drop(columns=["valor_pago"], errors="ignore")
    else:
        fat["valor_pago_sum"] = 0.0

    fat["status_norm"] = fat.get("status", "").apply(safe_lower)

    fat["recebido_calc"] = fat.apply(
        lambda r: float(r["valor_pago_sum"])
        if float(r["valor_pago_sum"]) > 0
        else (float(r["valor"]) if r["status_norm"] in ["pago", "paga", "paid"] else 0.0),
        axis=1,
    )
    return fat

def get_param_margem(params_df: pd.DataFrame, default: float = 0.45) -> float:
    if params_df is None or params_df.empty:
        return default
    tmp = params_df.copy()
    if "chave" not in tmp.columns or "valor" not in tmp.columns:
        return default
    tmp["chave"] = tmp["chave"].astype(str)
    row = tmp[tmp["chave"].str.strip().str.lower() == "margem_liquida_padrao"]
    if row.empty:
        return default
    try:
        return float(row.iloc[0]["valor"])
    except Exception:
        return default

def expected_revenue_projection(
    contratos_df: pd.DataFrame,
    start_month: date,
    months: int,
    avg_setup: float,
    avg_mrr: float,
    new_clients_per_month: int
) -> pd.DataFrame:
    con = contratos_df.copy()

    if "status_contrato" in con.columns:
        con["status_norm"] = con["status_contrato"].apply(safe_lower)
        active_mask = con["status_norm"].isin(["ativo", "ativa", "active"])
    else:
        active_mask = pd.Series([False] * len(con))

    con_active = con[active_mask].copy()
    con_active["mrr_valor"] = pd.to_numeric(con_active.get("mrr_valor", 0), errors="coerce").fillna(0.0)
    baseline_mrr = float(con_active["mrr_valor"].sum())

    rows = []
    current_new_clients = 0
    for i in range(months):
        m = add_months(start_month, i)
        current_new_clients += new_clients_per_month

        month_mrr_new = current_new_clients * float(avg_mrr)
        month_setup_new = new_clients_per_month * float(avg_setup)

        total = baseline_mrr + month_mrr_new + month_setup_new
        rows.append({"mes": m, "faturamento_projetado": float(total), "mes_label": month_label(m)})

    return pd.DataFrame(rows)

# =========================
# SIDEBAR (SIMPLES)
# =========================
st.sidebar.markdown("### Gestão Outside")
st.sidebar.markdown(
    f"<span class='badge'><span class='badge-dot'></span> Tema <strong class='orange'>{ACCENT}</strong></span>",
    unsafe_allow_html=True
)
st.sidebar.write("")

uploaded = st.sidebar.file_uploader(
    "📊 Base de dados (xlsx)",
    type=["xlsx"],
    help="Envie seu arquivo Excel com as abas: CLIENTES, CONTRATOS, FATURAMENTO, PAGAMENTOS, PARAMETROS",
)

horizon = st.sidebar.selectbox("Horizonte de projeção (meses)", [6, 12, 18, 24], index=1)

# =========================
# SELECIONAR ARQUIVO (PADRÃO OU UPLOAD)
# =========================
if uploaded is not None:
    file_source = uploaded
    usando_exemplo = False
else:
    # Tenta usar arquivo de dados principal
    try:
        file_source = "controle_clientes_preenchido_com_recebidos.xlsx"
        # Verifica se o arquivo existe
        with open(file_source, 'rb'):
            usando_exemplo = False
    except FileNotFoundError:
        # Se não encontrar o principal, tenta o de exemplo
        try:
            file_source = "exemplo_dados.xlsx"
            with open(file_source, 'rb'):
                usando_exemplo = True
        except FileNotFoundError:
            st.warning("⚠️ Nenhum arquivo encontrado")
            st.info(
                """
                ### Como usar este dashboard:
                
                1. **Prepare seu arquivo Excel** com as seguintes abas:
                   - `CLIENTES`: ID e nome dos clientes
                   - `CONTRATOS`: Contrato, cliente, status, setup, MRR
                   - `FATURAMENTO`: Fatura, cliente, valor, competência
                   - `PAGAMENTOS`: Pagamento, fatura, valor pago
                   - `PARAMETROS`: Configurações (ex: margem_liquida_padrao=0.45)
                
                2. **Faça upload** usando o botão acima
                
                3. Visualize suas métricas financeiras em tempo real!
                """
            )
            st.stop()

if usando_exemplo:
    st.sidebar.info("📌 Usando dados de exemplo. Faça upload para visualizar seus dados!")

# =========================
# DADOS + MÉTRICAS (GERAL)
# =========================
clientes, contratos, faturamento, pagamentos, params = load_data(file_source)
margem = get_param_margem(params, default=0.45)

fat = compute_received(faturamento, pagamentos)

hoje = date.today()
mes_atual = month_start(hoje)

total_recebido = float(fat["recebido_calc"].sum())
total_previsto_receber = float(fat["valor"].sum())
total_em_aberto = max(0.0, total_previsto_receber - total_recebido)

contratos["status_norm"] = contratos["status_contrato"].apply(safe_lower) if "status_contrato" in contratos.columns else ""
ativos = contratos[contratos["status_norm"].isin(["ativo", "ativa", "active"])].copy()
ativos["mrr_valor"] = pd.to_numeric(ativos.get("mrr_valor", 0), errors="coerce").fillna(0.0)
mrr_total = float(ativos["mrr_valor"].sum())

fat_mes = fat[fat["competencia_mes"] == mes_atual].copy()
faturado_mes = float(fat_mes["valor"].sum())
recebido_mes = float(fat_mes["recebido_calc"].sum())
em_aberto_mes = max(0.0, faturado_mes - recebido_mes)

lucro_recebido_total = total_recebido * margem
lucro_previsto_total = total_previsto_receber * margem
lucro_recebido_mes = recebido_mes * margem
lucro_previsto_mes = faturado_mes * margem

# séries mensais
serie = (
    fat.dropna(subset=["competencia_mes"])
    .groupby("competencia_mes", as_index=False)
    .agg(faturado=("valor", "sum"), recebido=("recebido_calc", "sum"))
    .sort_values("competencia_mes")
)
serie["mes_label"] = serie["competencia_mes"].apply(month_label)

# projeções
avg_setup = float(pd.to_numeric(ativos.get("setup_valor", 0), errors="coerce").fillna(0.0).mean()) if not ativos.empty else 0.0
avg_mrr = float(pd.to_numeric(ativos.get("mrr_valor", 0), errors="coerce").fillna(0.0).mean()) if not ativos.empty else 0.0
start_proj = add_months(mes_atual, 1)

proj_pior = expected_revenue_projection(contratos, start_proj, horizon, avg_setup, avg_mrr, new_clients_per_month=1)
proj_melhor = expected_revenue_projection(contratos, start_proj, horizon, avg_setup, avg_mrr, new_clients_per_month=3)

# =========================
# TOPO (LOGO + TÍTULO)
# =========================
top_left, top_right = st.columns([0.18, 0.82], vertical_alignment="center")

with top_left:
    if os.path.exists(LOGO_PATH):
        st.image(LOGO_PATH, use_container_width=True)
    else:
        st.markdown(
            f"<div class='metric-card' style='padding:14px; text-align:center;'>"
            f"<div class='metric-title'>Logo</div>"
            f"<div style='font-size:14px; color:rgba(245,245,247,0.75)'>Coloque <b>{LOGO_PATH}</b><br>na pasta do app</div>"
            f"</div>",
            unsafe_allow_html=True
        )

with top_right:
    st.markdown(
        f"<div style='display:flex; justify-content:space-between; align-items:flex-end; gap:12px;'>"
        f"<div>"
        f"<h1 style='margin:0; font-size:46px;'>Dashboard Financeiro</h1>"
        f"<div class='small-muted'>Visão geral, sem filtros, com base no que já entrou e no que ainda vai entrar (aba FATURAMENTO).</div>"
        f"</div>"
        f"<div class='badge'><span class='badge-dot'></span> Margem líquida: <strong class='orange'>{int(margem*100)}%</strong></div>"
        f"</div>",
        unsafe_allow_html=True
    )

st.markdown("<div class='hr'></div>", unsafe_allow_html=True)

# =========================
# COMPONENTE DE CARD (HTML)
# =========================
def card(title: str, value: str, sub: str = ""):
    sub_html = f"<div class='metric-sub'>{sub}</div>" if sub else ""
    return f"""
    <div class="metric-card">
      <div class="metric-title">{title}</div>
      <div class="metric-value">{value}</div>
      {sub_html}
    </div>
    """

# =========================
# KPIs (GERAL)
# =========================
r1 = st.columns(4)
r1[0].markdown(card("Recebido até agora", brl(total_recebido)), unsafe_allow_html=True)
r1[1].markdown(card("Previsto a receber (total lançado)", brl(total_previsto_receber), "Pago + em aberto, conforme FATURAMENTO"), unsafe_allow_html=True)
r1[2].markdown(card("Em aberto (a receber)", brl(total_em_aberto)), unsafe_allow_html=True)
r1[3].markdown(card("MRR atual (soma das mensalidades)", brl(mrr_total)), unsafe_allow_html=True)

st.markdown("<div class='hr'></div>", unsafe_allow_html=True)

# KPIs (MÊS)
r2 = st.columns(4)
r2[0].markdown(card(f"Faturado no mês ({month_label(mes_atual)})", brl(faturado_mes)), unsafe_allow_html=True)
r2[1].markdown(card(f"Recebido no mês ({month_label(mes_atual)})", brl(recebido_mes)), unsafe_allow_html=True)
r2[2].markdown(card(f"Em aberto no mês ({month_label(mes_atual)})", brl(em_aberto_mes)), unsafe_allow_html=True)
r2[3].markdown(card("Ticket médio (ativos)", f"{brl(avg_setup)} setup", f"{brl(avg_mrr)} MRR médio"), unsafe_allow_html=True)

st.markdown("<div class='hr'></div>", unsafe_allow_html=True)

# KPIs (LUCRO)
r3 = st.columns(4)
r3[0].markdown(card("Lucro sobre recebido (total)", brl(lucro_recebido_total)), unsafe_allow_html=True)
r3[1].markdown(card("Lucro sobre previsto (total)", brl(lucro_previsto_total)), unsafe_allow_html=True)
r3[2].markdown(card("Lucro sobre recebido (mês)", brl(lucro_recebido_mes)), unsafe_allow_html=True)
r3[3].markdown(card("Lucro sobre faturado (mês)", brl(lucro_previsto_mes)), unsafe_allow_html=True)

st.markdown("<div class='hr'></div>", unsafe_allow_html=True)

# =========================
# GRÁFICOS (Faturado vs Recebido)
# =========================
g1, g2 = st.columns(2)

with g1:
    st.subheader("Faturado vs Recebido (mensal)")
    if serie.empty:
        st.info("Sem dados suficientes para montar a série mensal.")
    else:
        if px is not None:
            df_long = serie.melt(id_vars=["competencia_mes", "mes_label"], value_vars=["faturado", "recebido"], var_name="tipo", value_name="valor")
            fig = px.line(df_long, x="competencia_mes", y="valor", color="tipo", markers=True)
            fig.update_layout(
                paper_bgcolor="rgba(0,0,0,0)",
                plot_bgcolor="rgba(0,0,0,0)",
                font_color="#F5F5F7",
                legend_title_text="",
                xaxis_title="Competência",
                yaxis_title="Valor",
            )
            # deixa uma linha laranja e outra branca
            fig.for_each_trace(lambda t: t.update(line=dict(color=ACCENT)) if t.name == "faturado" else t.update(line=dict(color="#F5F5F7")))
            st.plotly_chart(fig, use_container_width=True)
        st.dataframe(
            serie[["mes_label", "faturado", "recebido"]].rename(columns={"mes_label": "Mês", "faturado": "Faturado", "recebido": "Recebido"}),
            use_container_width=True,
            hide_index=True,
        )

with g2:
    st.subheader("Previsões de faturamento")
    st.markdown(
        f"<span class='badge'><span class='badge-dot'></span> Pior hipótese: <strong class='orange'>+1 cliente/mês</strong></span>"
        f" &nbsp; "
        f"<span class='badge'><span class='badge-dot'></span> Melhor hipótese: <strong class='orange'>+3 clientes/mês</strong></span>",
        unsafe_allow_html=True
    )
    if px is not None and not proj_pior.empty and not proj_melhor.empty:
        proj_pior2 = proj_pior.copy()
        proj_pior2["cenario"] = "Pior (1 cliente/mês)"
        proj_melhor2 = proj_melhor.copy()
        proj_melhor2["cenario"] = "Melhor (3 clientes/mês)"
        proj_all = pd.concat([proj_pior2, proj_melhor2], ignore_index=True)

        fig = px.line(proj_all, x="mes", y="faturamento_projetado", color="cenario", markers=True)
        fig.update_layout(
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            font_color="#F5F5F7",
            legend_title_text="",
            xaxis_title="Mês",
            yaxis_title="Faturamento projetado",
        )
        fig.for_each_trace(lambda t: t.update(line=dict(color=ACCENT)) if "Pior" in t.name else t.update(line=dict(color="#F5F5F7")))
        st.plotly_chart(fig, use_container_width=True)

    pcol1, pcol2 = st.columns(2)
    with pcol1:
        st.caption("Pior hipótese (1 cliente/mês)")
        st.dataframe(
            proj_pior[["mes_label", "faturamento_projetado"]].rename(columns={"mes_label": "Mês", "faturamento_projetado": "Faturamento projetado"}),
            use_container_width=True,
            hide_index=True
        )
    with pcol2:
        st.caption("Melhor hipótese (3 clientes/mês)")
        st.dataframe(
            proj_melhor[["mes_label", "faturamento_projetado"]].rename(columns={"mes_label": "Mês", "faturamento_projetado": "Faturamento projetado"}),
            use_container_width=True,
            hide_index=True
        )

st.markdown("<div class='hr'></div>", unsafe_allow_html=True)

# =========================
# RESUMO POR CLIENTE (GERAL)
# =========================
st.subheader("Resumo por cliente (geral)")
fat_cli = fat.merge(clientes[["cliente_id", "cliente"]], on="cliente_id", how="left")
resumo_cliente = (
    fat_cli.groupby(["cliente_id", "cliente"], as_index=False)
    .agg(total_previsto=("valor", "sum"), total_recebido=("recebido_calc", "sum"))
)
resumo_cliente["em_aberto"] = resumo_cliente["total_previsto"] - resumo_cliente["total_recebido"]
resumo_cliente = resumo_cliente.sort_values("total_previsto", ascending=False)

resumo_cliente_view = resumo_cliente.copy()
resumo_cliente_view["total_previsto"] = resumo_cliente_view["total_previsto"].apply(brl)
resumo_cliente_view["total_recebido"] = resumo_cliente_view["total_recebido"].apply(brl)
resumo_cliente_view["em_aberto"] = resumo_cliente_view["em_aberto"].apply(lambda x: brl(max(0.0, x)))

st.dataframe(
    resumo_cliente_view[["cliente", "total_previsto", "total_recebido", "em_aberto"]].rename(
        columns={
            "cliente": "Cliente",
            "total_previsto": "Previsto (total lançado)",
            "total_recebido": "Recebido",
            "em_aberto": "Em aberto",
        }
    ),
    use_container_width=True,
    hide_index=True,
)

st.caption("Logo: coloque o arquivo logogo.jpg na mesma pasta do app. Projeções usam ticket médio dos contratos ativos (setup médio e MRR médio).")