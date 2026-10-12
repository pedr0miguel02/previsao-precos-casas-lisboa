# Dados

Os dados não estão incluídos neste repositório (estão excluídos pelo `.gitignore`).

| Pasta | Conteúdo |
|---|---|
| `raw/` | Ficheiros originais de anúncios (`dataset_*.csv`) |
| `processed/` | Dados limpos, criados pelo notebook `01_limpeza_dados.ipynb` |

## Como reproduzir

1. Obter um ficheiro CSV com anúncios de apartamentos à venda em Lisboa, com as colunas indicadas abaixo.
   Usa apenas dados que tenhas permissão para recolher e utilizar.
2. Guardar o ficheiro em `data/raw/` com um nome começado por `dataset_` (ex.: `dataset_2026-10-12.csv`).
3. Correr os notebooks pela ordem (01 → 04).

O notebook 01 usa automaticamente o ficheiro `dataset_*.csv` mais recente.

## Colunas esperadas na exportação

O notebook 01 usa estas colunas (formato "achatado": os subcampos aparecem separados por `/`):

`propertyCode`, `price`, `size`, `rooms`, `bathrooms`, `floor`, `hasLift`, `status`, `propertyType`, `newDevelopment`, `operation`, `municipality`, `district`, `latitude`, `longitude`, `features/hasTerrace`, `features/hasSwimmingPool`, `features/hasGarden`, `features/hasAirConditioning`, `features/hasBoxRoom`, `parkingSpace/hasParkingSpace`, `priceDropPercentage`, `url`
