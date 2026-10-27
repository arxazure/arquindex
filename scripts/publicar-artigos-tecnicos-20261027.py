"""Publica os artigos de 27/10/2026 reutilizando o publicador transacional validado."""
from pathlib import Path

template_path = Path(__file__).with_name("publicar-artigos-tecnicos-20261026.py")
code = template_path.read_text(encoding="utf-8")
replacements = [
    ("2026-10-26", "2026-10-27"),
    ("20261026", "20261027"),
    ("metadados-decreto-10278-indice-digitalizacao", "controlador-operador-digitalizacao-ropa-evidencias"),
    ("tipos-aspectos-pastas-alfresco-modelagem-documental", "transmittal-controle-revisoes-databook"),
    ("ARQ-ARTICLE-20261027-METADADOS-DECRETO-10278", "ARQ-ARTICLE-20261027-CONTROLADOR-OPERADOR-ROPA"),
    ("ARQ-ARTICLE-20261027-ALFRESCO-TIPOS-ASPECTOS-PASTAS", "ARQ-ARTICLE-20261027-TRANSMITTAL-REVISOES-DATABOOK"),
]
for old, new in replacements:
    if old not in code:
        raise RuntimeError(f"Modelo inesperado: marcador ausente: {old}")
    code = code.replace(old, new)

exec(compile(code, str(template_path), "exec"), {"__name__": "__main__", "__file__": str(template_path)})
