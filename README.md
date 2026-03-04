# Dashboard Financeiro - Gestão Outside

Dashboard interativo para visualização e análise de dados financeiros, construído com Streamlit.

**⚡ Quick Start**: Abra, veja dados de exemplo já funcionando, faça upload de seus dados quando quiser!

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

### Como usar

1. **Abra o app** - Ele já começa com dados de exemplo automaticamente 🎉
2. **Visualize as métricas** - Veja todos os gráficos e KPIs funcionando
3. **Faça upload** (opcional) - Use o botão no sidebar para visualizar seus próprios dados
4. **Ajuste projeções** - Use o seletor de horizonte (6, 12, 18 ou 24 meses)

### Arquivo de dados

Para usar seus próprios dados, prepare um arquivo Excel (.xlsx) com as seguintes abas:

| Aba | Colunas obrigatórias | Descrição |
|-----|----------------------|-----------|
| **CLIENTES** | `cliente_id`, `cliente` | IDs e nomes dos clientes |
| **CONTRATOS** | `contrato_id`, `cliente_id`, `status_contrato`, `setup_valor`, `mrr_valor` | Dados dos contratos |
| **FATURAMENTO** | `fatura_id`, `cliente_id`, `valor`, `competencia` | Faturas emitidas |
| **PAGAMENTOS** | `pagamento_id`, `fatura_id`, `valor_pago` | Pagamentos recebidos |
| **PARAMETROS** | `chave`, `valor` | Configurações (ex: `margem_liquida_padrao`) |

**Dica:** O arquivo `exemplo_dados.xlsx` está incluído e é carregado automaticamente. Use como template para suas próprias dados.

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

---

## ✅ Próximos passos para publicar no Streamlit Cloud

Veja [INSTRUCOES_GITHUB.md](INSTRUCOES_GITHUB.md) para um passo a passo completo de como:
1. Criar repositório no GitHub
2. Fazer push do código
3. Publicar no Streamlit Community Cloud
