# Espanha: RGPD, LOPDGDD e governação de IA em ECM

**Arquindex Academy — Alfresco AI** | Atualizado: 07/11/2026 | Idioma editorial: es-ES
**Escopo:** referência técnico-educacional para consultoria B2B; não constitui parecer jurídico ou declaração de certificação.

## 1. Contexto regulatório e prática empresarial
Para fluxos documentais, identificar base jurídica, minimização, limitações de conservação, direitos dos titulares, segurança, avaliação de impacto quando aplicável e transferências internacionais. No AI Act, mapear papéis de fornecedor e utilizador (deployer) e classe de risco; não inferir que qualquer OCR seja um sistema de alto risco.

## 2. Fontes primárias e autoridades
- [RGPD](https://eur-lex.europa.eu/eli/reg/2016/679/oj)
- [Ley Orgánica 3/2018 LOPDGDD](https://www.boe.es/buscar/act.php?id=BOE-A-2018-16673)
- [AI Act da União Europeia](https://digital-strategy.ec.europa.eu/en/policies/enforcement-ai-act)
- [AEPD](https://www.aepd.es/)

## 3. Como aplicar em projetos Alfresco ECM + Document AI
1. **Inventário:** identificar controlador/responsável, finalidades, categorias de dados e sistemas que fazem tratamento.
2. **Classificação:** criar tipologias documentais e regras de retenção fundamentadas, não prazos inventados.
3. **Permissões:** configurar autenticação e autorização por identidade, função e cliente; testar segregação multiempresa.
4. **Document Intelligence:** processar OCR em workers isolados, registrar hash SHA-256 do arquivo original e versão de cada derivado.
5. **IA:** definir objetivo, localização de processamento, modelo utilizado, governança dos prompts e verificação de saída; evitar envio de dados sensíveis a serviços externos sem avaliação e autorização.
6. **Auditoria e direitos:** registrar acesso e alterações, garantir rastreabilidade, suportar pedidos de titulares conforme enquadramento aplicável.
7. **Segurança:** aplicar TLS, backups testados, gestão de segredos, revisão de fornecedores e plano de resposta a incidentes.
8. **Avaliação jurídica:** conferir requisitos setoriais, contratos, transferências, obrigações legais e eventuais períodos transitórios com especialista local.

## 4. Exemplo de arquitetura e caso prático
Use um mapa de dados por tipo documental e configure regras de acesso, retenção, eliminação segura e revisão humana de resultados gerados por modelos.

```text
Usuário autenticado
  -> Alfresco ECM (permissões / ciclo de vida)
  -> fila OCR isolada (Tesseract)
  -> armazenamento original + SHA-256
  -> PostgreSQL (metadados / trilha de auditoria)
  -> IA local (Ollama), com filtragem por permissões
  -> revisão humana e relatório
```

## 5. Checklist de testes técnicos
- [ ] Documento de um cliente não é recuperável por usuário de outro cliente.
- [ ] A revogação de acesso no ECM também bloqueia a camada de busca/IA.
- [ ] Alterações no conteúdo original são detectadas por novo hash.
- [ ] Prompts contidos em documentos não podem modificar permissões.
- [ ] OCR e IA guardam identificação da versão e permitem revisão.
- [ ] Backups e restauração são exercitados em ambiente separado.
- [ ] Bases legais e prazos de retenção são validados por jurisdição.

## 6. Exercício comentado
**Pergunta:** É suficiente armazenar SHA-256 para provar conformidade legal?

**Resposta:** Não. O hash demonstra consistência dos bytes em comparação com um valor confiável; não comprova identidade do autor, legitimidade da coleta, base legal, consentimento, cadeia de custódia ou respeito a direitos dos titulares.

## Leia também
- [Central da Arquindex Academy – Alfresco AI](../README.md)
- [Arquitetura de Alfresco + IA](../01-alfresco-ai.md)
- [Laboratório FastAPI e PostgreSQL](../02-fastapi-postgresql.md)
- [Laboratório SHA-256](../03-digital-evidence.md)
- [Portugal: RGPD, ciberseguranca e IA empresarial](portugal-rgpd-nis2-ai-act.md)
- [Argentina: Ley 25.326, privacidad y sistemas de IA documental](argentina-ley-25326-ia-documental.md)
- [México: LFPDPPP 2025, avisos de privacidad y gestión documental segura](mexico-lfpdppp-2025-ecm.md)
- [Panamá: Ley 81/2019, Decreto 285/2021 y gobernanza documental](panama-ley81-datos-seguridad-ia.md)

*Revisão editorial e jurídica recomendada antes de replicar em ambiente corporativo. Os textos são gerais e não substituem a legislação consolidada e orientações das autoridades.*
