# Integração Alfresco — temporalidade e relatório de produção

## Estado
Código isolado para revisão e integração. **Não implantado no conector principal.**
O Railway `conector-alfresco-arquindex` contém uma função Bun proxy para
`https://conectoralfresco.arquindex-capture.stream`, e não o backend da importação.

## Como integrar com o backend real
1. Importar os tipos aprovados da TTDD SMS por código, sob versão e aprovação.
   Atestado Médico `01.20.006.001`: evento **desligamento**, **10 anos** após o evento;
   dados pessoais sensíveis, restrição de acesso real via ACL.
2. Após upload concluir e receber o `nodeId` do Alfresco, aplicar aspectos e propriedades
   usando o modelo de conteúdo registrado no repositório. Não inventar namespace/QNames:
   ler o modelo real. Utilizar PUT /alfresco/api/-default-/public/alfresco/versions/1/nodes/{nodeId}
   com os aspectos e propriedades suportados, preservando aspectos existentes.
3. Confirmar em GET no mesmo nodeId que regras, classificação e propriedades persistiram.
   Sem GET confirmatório, não marcar `VALIDADO` nem `APLICADA`.
4. `dataEvento` vem do desligamento confirmado; não usar data de upload ou emissão.
   Sem evento: `AGUARDANDO_EVENTO`; data de avaliação = null. Se prazo da TTDD
   não estiver aprovado, `REGRA_PENDENTE`; não transformar todo documento em `PRAZO_A_VALIDAR`.
5. Registrar eventos imutáveis de recebimento, gravação, validação e erro com idempotência,
   segregação por empresa e departamento e trilha de auditoria, evitando exposição de
   nomes de pacientes ou informações clínicas nos relatórios.
6. Persistir eventos no banco operacional: este módulo apenas avalia e agrega entradas,
   não consulta automaticamente o Alfresco, e não grava em produção.
7. Atualização retrospectiva por lote, modo prévia antes de efetivar, limite por execução,
   backup, resultado por documento e possibilidade de retomada; jamais eliminar arquivos.
8. Validar com documentos de teste de departamento autorizado antes de produção.

## Relatório avançado
- Cards: recebidos, gravados, validados, falhas, duplicados, pendências,
  temporalidade aplicada/pendente, páginas e bytes conhecidos.
- Agrupamentos: empresa, departamento, classificação, tipo, operador e lote.
- Drilldown: id do evento/documento, lote, nome do arquivo, horário, nodeId e status.
- Filtros de período, site, departamento, operador, lote, tipo e status deverão ser
  implementados na camada de consulta, respeitando as permissões de acesso.
- Exportar CSV/XLSX/PDF via backend autenticado com dados filtrados e auditados.
- Não confundir 'gravado' com 'validado', nem 'regra aplicada' com 'evento ocorrido'.

## Testes
Na branch, executar `bun test integracoes/alfresco/temporalidade-producao.test.ts`.
