# 📊 RECOMENDAÇÕES DE COLUNAS PARA EXPLORAÇÃO

## Resumo Executivo
- **Total de registros:** 5.673
- **Total de colunas:** 89
- **Colunas com 100% completas:** 34
- **Colunas com >95% completas:** 59

---

## 🎯 COLUNAS RECOMENDADAS (100% COMPLETAS - SEM RISCO DE ALUCINAÇÃO)

### 1. **Colunas Geoespaciais** ⭐⭐⭐ (PRIORITÁRIAS)
Essas são EXCELENTES para análise sem vazios:

- `longitude` - Coordenada X (100%)
- `latitude` - Coordenada Y (100%)
- `NUM_LONGIT` - Número longitude original (100%)
- `NUM_LATITU` - Número latitude original (100%)
- `DS_WKT` - Geometria em formato WKT (100%)
- `DES_LOCAL_` - Descrição textual da localização (100%)

**Por quê usar?** Todas têm cobertura 100%, permitindo análises espaciais seguras:
- Mapas de calor por infração
- Clustering geográfico
- Análise de proximidade
- Correlação com biomas e territórios indígenas

---

### 2. **Colunas de Identificação da Infração** ⭐⭐⭐

- `COD_INFRAC` - Código da infração (100%)
- `DES_INFRAC` - Descrição da infração (100%)
- `TIPO_INFRA` - Tipo de infração (100%)
- `CD_RECEITA` - Código de receita (100%)
- `DES_RECEIT` - Descrição da receita/penalidade (100%)

**Por quê usar?** Dados categóricos precisos sem lacunas:
- Tipos de infração mais comuns por região
- Análise de penalidades associadas
- Clustering de tipos de crime

---

### 3. **Colunas Temporais** ⭐⭐⭐

- `DAT_HORA_A` - Data/hora da autuação (100%)
- `DT_FATO_IN` - Data do fato infracional (100%)
- `DT_INICIO_` - Data início do ato inequívoco (100%)
- `DT_FIM_ATO` - Data fim do ato (100%)
- `DT_LANCAME` - Data de lançamento (100%)
- `DT_ULT_ALT` - Data última alteração (100%)
- `parsed_dat` - Data parseada (100%)

**Por quê usar?** Série temporal completa:
- Análise de tendências de infrações
- Padrões sazonais
- Comparação entre períodos
- Timeline de processos

---

### 4. **Colunas de Localização Administrativa** ⭐⭐

- `COD_MUNICI` - Código do município (100%)
- `MUNICIPIO` - Nome do município (100%)
- `UF` - Unidade Federativa (100%)
- `UNID_CONTR` - Unidade de controle/fiscalização (100%)

**Por quê usar?** Geografia administrativa sem vazios:
- Ranking de municípios com mais infrações
- Distribuição por estado
- Análise de efetividade da fiscalização por região

---

### 5. **Colunas de Infratores** ⭐⭐

- `NOME_INFRA` - Nome do infrator (100%)
- `NUM_PESSOA` - Número de pessoa (100%)
- `TP_PESSOA_` - Tipo de pessoa (99.9%)
- `CPF_CNPJ_I` - CPF/CNPJ (99.9%)

**Por quê usar?** Dados de infratores praticamente completos:
- Identificar reincidentes
- Análise de padrões comportamentais
- Perfil de infratores (PJ vs PF)

---

### 6. **Colunas de Status e Processo** ⭐⭐

- `DS_SIT_AUT` - Situação da autuação (100%) → Valores: "Impresso" (99.4%), "Excluído" (0.5%)
- `SIT_CANCEL` - Situação cancelamento (100%) → Valores: "N" (97%), "S" (3%)
- `NUM_AUTO_I` - Número da autuação (100%) - Identificador único
- `DES_STATUS` - Descrição do status (99.6%)
- `TIPO_ACAO` - Tipo de ação (99.6%)
- `PASSIVEL_R` - Passível de recurso (99.6%)

**Por quê usar?** Rastreamento processual sem lacunas:
- Taxa de cancelamento de multas
- Análise de recursos interpostos
- Identificar ações mais efetivas

---

### 7. **Colunas Temáticas Ambientais** ⭐⭐

- `DS_BIOMAS_` - Descrição do bioma (99.0%)
- `ID_SICAFI_` - ID SICAFI (99.0%)

**Por quê usar?** Associação com biomas:
- Infrações por tipo de bioma
- Hotspots de desmatamento por bioma

---

## ⚠️ COLUNAS COM CAUTION (>80% - USE COM CUIDADO)

### Baixa Completude (pode gerar alucinação):

| Coluna | Completude | Uso Recomendado |
|--------|-----------|-----------------|
| `TIPO_MULTA` | 92.4% | Análise de penalidades (3% de risco) |
| `DS_REFEREN` | 88.6% | Contexto de infrações (11% de risco) |
| `DAT_CIENCI` | 86.6% | Datas de ciência (13% de risco) |
| `CLASSIFICA` | 97.5% | Classificação de infrações (2.5% de risco) |
| `GRAVIDADE_` | 47.8% | ❌ Evitar - metade dos dados vazios |
| `DS_ENQUADR` | 25.7% | ❌ Evitar - 3/4 dos dados vazios |

---

## 🚫 COLUNAS PARA EVITAR TOTALMENTE

Muito incompletas (podem induzir sérios vieses):

- `DES_OUTROS` (0.0%)
- `DS_FATOR_A` (0.0%)
- `DENUNCIA_S` (0.0%)
- `SER_AUTO_I` (0.0%)
- `PATRIMONIO` (0.0%)
- `WKT_GE_ARE` (0.9%)
- `QT_AREA` (0.7%)
- `UNIDADE_CO` (0.7%)

---

## 📈 MATRIZ DE ANÁLISE RECOMENDADA

### Análise 1: Espacial
```
Dimensões: longitude, latitude, MUNICIPIO, TIPO_INFRA
Métricas: contagem, densidade
```

### Análise 2: Temporal
```
Dimensões: parsed_dat, TIPO_INFRA, UF
Métricas: série temporal, tendências
```

### Análise 3: Infratores
```
Dimensões: NOME_INFRA, TP_PESSOA_, TIPO_INFRA
Métricas: reincidência, padrões
```

### Análise 4: Efetividade
```
Dimensões: MUNICIPIO, UF, TIPO_ACAO, DES_STATUS
Métricas: taxa de resolução, cancelamentos
```

---

## 💡 MELHOR ESTRATÉGIA PARA EVITAR ALUCINAÇÃO

1. **Use APENAS as 34 colunas com 100% de dados** como base
2. **Combine com colunas >95%** para enriquecer análise
3. **Evite análises que dependem das colunas <85%** de completude
4. **Sempre filtre registros com dados vazios** antes de análises específicas
5. **Documente qual coluna completude você usou** em cada conclusão

---

## 📊 Valor de Cobertura por Tipo de Análise

| Tipo de Análise | Melhor Coluna Base | Cobertura |
|------------------|-------------------|-----------|
| Geoespacial | latitude, longitude | 100% |
| Temporal | DT_FATO_IN | 100% |
| Infrator | NOME_INFRA | 100% |
| Infração | COD_INFRAC | 100% |
| Localização | MUNICIPIO | 100% |
| Status | DS_SIT_AUT | 100% |

