# 📤 Próximos Passos: Subir para GitHub

Seu projeto local já está preparado com git! Siga os passos abaixo para subir no GitHub e publicar no Streamlit Community Cloud.

## 1️⃣ Criar repositório no GitHub

1. Acesse [github.com](https://github.com) e faça login
2. Clique em "+" (canto superior direito) → "New repository"
3. Nome do repositório: `dashboard-financeiro` (ou escolha um nome)
4. Descrição: "Dashboard Financeiro - Gestão Outside com Streamlit"
5. Escolha **público** (para publicar no Streamlit Community Cloud)
6. **NÃO** selecione "Initialize this repository with README" (já temos)
7. Clique em "Create repository"

## 2️⃣ Fazer push do código para GitHub

Copie e execute estes comandos no terminal:

```bash
cd "/Users/zemuller/Documents/Dash financeiro GO"

# Adicione a origem remota (substitua SEU_USUARIO pelo seu user GitHub)
git remote add origin https://github.com/SEU_USUARIO/dashboard-financeiro.git

# Renomeie branch para main (se necessário)
git branch -M main

# Faça push
git push -u origin main
```

**Exemplo prático:**
```bash
git remote add origin https://github.com/joaosilva/dashboard-financeiro.git
git branch -M main
git push -u origin main
```

## 3️⃣ Publicar no Streamlit Community Cloud

1. Acesse [Streamlit Community Cloud](https://share.streamlit.io)
2. Clique em "New app"
3. Selecione:
   - **Repository**: seu_usuario/dashboard-financeiro
   - **Branch**: main
   - **Main file path**: app_gestao_outside_dashboard.py
4. Clique em "Deploy"

Pronto! ✅ Seu dashboard estará publicado em poucos minutos.

## 📝 Instruções para reatualizar após mudanças

Quando fizer alterações no código:

```bash
cd "/Users/zemuller/Documents/Dash financeiro GO"
git add .
git commit -m "Descrição da mudança"
git push
```

O Streamlit Community Cloud atualiza automaticamente a cada push!

---

**Dúvidas?**
- Documentação GitHub: https://docs.github.com
- Streamlit Cloud: https://docs.streamlit.io/deploy/streamlit-community-cloud
