# IGSA · Gestão de Prazos Preclusivos

Painel Streamlit da Controladoria Jurídica — **Imaculada Gordiano Sociedade de Advogados**.

App único (`app.py`) que carrega a exportação do LegalOne (`.xlsx`), aplica as regras de
negócio da Controladoria, publica os dados e exibe o painel público (Visão Geral, Por
Coordenação, Auditoria e Exportação). Toda a lógica segue o **Manual de Configuração —
Revisão 2 (Junho/2026)**.

## Executar localmente

```bash
pip install -r requirements.txt
streamlit run app.py
```

Numa cópia recém-clonada, o painel abre **sem nenhum dado publicado** — é preciso fazer
a primeira carga em **Área Administrativa → Carregar planilha → Publicar**.

`dados_publicados.json` (e os arquivos de aprendizado `coord_aprendido.json`,
`nomes_corrigidos.json`, `responsaveis_nao_importar.json`) são **dados de uso, não
código-fonte** — por isso ficam fora do controle de versão (`.gitignore`). Versionar
esses arquivos na mesma branch do código fazia o app voltar à última carga commitada
a cada redeploy (todo push de código nesta branch reinicia o container do Streamlit
Cloud, que reclona o repositório do zero — e antes disso apagava qualquer publicação
feita ao vivo entre uma correção e outra).

## Fluxo de dados

1. **Área Administrativa** (uso interno): upload do `.xlsx` → validação automática →
   seleção manual de coordenador para responsáveis não mapeados → **Publicar** (grava
   `dados_publicados.json` localmente e, com `GITHUB_TOKEN` configurado nos Secrets do
   Streamlit Cloud, também no repositório `GITHUB_REPO` — importante para não perder a
   carga caso o container seja recriado).
2. **Painel público**: lê `dados_publicados.json` e exibe cards, gráficos, tabelas
   coloridas por prazo e a tabela **Prazos por responsável**.

## Onde ajustar as configurações (Manual, seção 18)

Tudo fica no topo de `app.py`, no bloco **CONSTANTES**:

| Item | Constante |
|------|-----------|
| A/B · Coordenadores e executores | `COORD_MAP` |
| C · Responsável inativo | _descontinuado — sem filtro por status de responsável_ |
| D · Excluir dos painéis | `EXCLUDED_SET` |
| E · Ocultar coordenação | `HIDDEN_COORDS` |
| F · Normalização de tipos | `normalizar_tipo()` |
| G · Feriados (virada de ano) | `HOLIDAYS_2026` / `HOLIDAYS_NP` |
| H · Horizonte do filtro (DU ≤ 1) | `DU_LIMIT` |
| I · Repositório de publicação | `GITHUB_REPO` |

## Estrutura

```
app.py                     # aplicação Streamlit (dados + UI redesenhada)
dados_publicados.json      # carga publicada (gerado em runtime — fora do Git)
requirements.txt
project/                   # bundle de design original + assets + planilhas de teste
```
