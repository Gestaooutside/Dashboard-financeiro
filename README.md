# Dashboard Financeiro - Gestão Outside

Dashboard interativo para visualização e análise de dados financeiros, construído com Streamlit.

## Características

- 📊 Visualização de faturamento vs recebimentos (mensal)
- 💰 KPIs financeiros (recebido, previsto, em aberto, MRR)
- 📈 Cálculo de lucro baseado em margem configurável
- 🔮 Projeções de faturamento (cenários pior e melhor)
- 👥 Resumo detalhado por cliente
- 🎨 Interface premium com tema preto e laranja

## Requisitos

- Python 3.8+
- pandas
- streamlit
- plotly
- python-dateutil
- openpyxl

## Instalação

1. Clone o repositório:
```bash
git clone https://github.com/seu-usuario/dashboard-financeiro.git
cd dashboard-financeiro
```

2. Crie um ambiente virtual:
```bash
python -m venv venv
source venv/bin/activate  # No Windows: venv\Scripts\activate
```

3. Instale as dependências:
```bash
pip install -r requirements.txt
```

## Uso

Execute o dashboard com:
```bash
streamlit run app_gestao_outside_dashboard.py
```

O app será aberto em `http://localhost:8501`

### Arquivo de dados

O dashboard espera um arquivo Excel (.xlsx) com as seguintes abas:
- **CLIENTES**: ID do cliente, nome, etc
- **CONTRATOS**: ID contrato, cliente_id, status_contrato, setup_valor, mrr_valor
- **FATURAMENTO**: ID fatura, cliente_id, valor, competencia, data_pagamento
- **PAGAMENTOS**: ID pagamento, fatura_id, valor_pago, data_pagamento
- **PARAMETROS**: chave, valor (ex: chave="margem_liquida_padrao", valor=0.45)

Por padrão, o app carrega `controle_clientes_preenchido_com_recebidos.xlsx` se nenhum arquivo for upload.

## Publicar no Streamlit Community Cloud

1. Faça push deste repositório para GitHub
2. Acesse [Streamlit Community Cloud](https://streamlit.io/cloud)
3. Clique em "New app"
4. Selecione este repositório e a branch `main`
5. Define o arquivo principal como: `app_gestao_outside_dashboard.py`
6. Clique em "Deploy"

## Configuração

- **Logo**: Coloque um arquivo chamado `logogo.jpg` na pasta do app
- **Margem padrão**: Configurável via planilha (aba PARAMETROS)
- **Horizonte de projeção**: Customizerável no sidebar (6-24 meses)

## Arquivos principais

- `app_gestao_outside_dashboard.py` - App principal
- `bibliotecas.py` - Configuração de bibliotecas
- `requirements.txt` - Dependências Python
- `.streamlit/` - Config do Streamlit

## Licença

MIT
