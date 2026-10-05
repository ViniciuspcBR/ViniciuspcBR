"""Retoca o SVG do calendário isométrico gerado pelo metrics.

Uso: python3 patch-isocalendar.py caminho/do/arquivo.svg
"""
import sys
from pathlib import Path

ARQUIVO = Path(sys.argv[1])

# Marca para saber se o arquivo já foi retocado (evita aplicar duas vezes)
MARCA = "/* perfil-custom */"

# Trecho que existe no fim do <style> do SVG; vamos colar o nosso CSS logo depois dele
ANCORA = "#metrics-end{width:100%}"

# O CSS que muda a aparência
CSS = (
    MARCA
    # Chão: troca o branco (#ebedf0) pelo cinza escuro dos quadradinhos vazios do GitHub (#161b22)
    + 'path[fill="#ebedf0"]{fill:#161b22}'
    # Legendas: a coluna da esquerda ocupa todo o espaço livre...
    + ".row section:first-child{flex:1 1 0}"
    # ...e a coluna das legendas só ocupa o tamanho do conteúdo, colada na direita
    + ".row section:last-child{flex:0 0 auto;margin-right:8px}"
)

svg = ARQUIVO.read_text(encoding="utf-8")

if MARCA in svg:
    print("SVG já estava retocado, nada a fazer.")
    sys.exit(0)

if ANCORA not in svg:
    # Não derruba o workflow: só avisa (o SVG original continua válido)
    print("::warning::Trecho de referência não encontrado no SVG; retoque ignorado.")
    sys.exit(0)

# Cola o CSS depois da âncora (apenas na primeira ocorrência) e salva
ARQUIVO.write_text(svg.replace(ANCORA, ANCORA + CSS, 1), encoding="utf-8")
print("SVG retocado com sucesso.")
