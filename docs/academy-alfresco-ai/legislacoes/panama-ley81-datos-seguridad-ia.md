# Panamá: Ley 81/2019, Decreto 285/2021 y gobernanza documental

**Arquindex Academy — Alfresco AI** | Atualizado: 07/11/2026 | Idioma editorial: es-PA
**Escopo:** referência técnico-educacional para consultoria B2B; não constitui parecer jurídico ou declaração de certificação.

## 1. Contexto regulatório e prática empresarial
A Ley 81 estabelece princípios, direitos e obrigações de tratamento de dados; o Decreto 285 regulamenta seu regime. Regras de IA devem ser tratadas separadamente: não presumir que um projeto de lei ou guia de boas práticas seja lei aprovada.

## 2. Fontes primárias e autoridades
- [Ley 81/2019 — Procuraduría](https://infojuridica.procuraduria-admon.gob.pa/norma_screen?numsec=52898)
- [Decreto Ejecutivo 285/2021](https://infojuridica.procuraduria-admon.gob.pa/norma_screen.php?numsec=56425)
- [ANTAI — legislação](https://antai.gob.pa/legislacion/)

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
Implementar classificação de dados, matriz de perfis, canal para pedidos de titulares, logs de acesso, política de temporalidade e revisão humana da extração por IA.

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
- [Espanha: RGPD, LOPDGDD e governação de IA em ECM](espana-rgpd-lopdgdd-ai-act.md)
- [Argentina: Ley 25.326, privacidad y sistemas de IA documental](argentina-ley-25326-ia-documental.md)
- [México: LFPDPPP 2025, avisos de privacidad y gestión documental segura](mexico-lfpdppp-2025-ecm.md)

*Revisão editorial e jurídica recomendada antes de replicar em ambiente corporativo. Os textos são gerais e não substituem a legislação consolidada e orientações das autoridades.*
