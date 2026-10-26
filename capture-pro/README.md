# Núcleo técnico de metadados — Arquindex Capture Pro

Este diretório contém implementação executável independente de captura e validação de metadados conforme o perfil do Anexo II do Decreto 10.278/2020. **Não é implantação na API do Railway**.

## Testes
```bash
node --test capture-pro/decreto10278.test.js
```

## Integração exigida
No serviço de captura autenticado, usar `registrarCaptura` com bytes reais do arquivo matriz, tenant e operador derivados da sessão do servidor, não de payload do navegador. Persistir o registro e as evidências em transação, com unicidade do UUID e políticas multi-tenant. Usar `finalizar` antes da transição de estado; validar assinatura ICP-Brasil, parâmetros de captura (Anexo I), logs e formatos aplicáveis separadamente.

Dados extraídos por OCR/IA devem ser sugestões revisáveis, sem sobrescrever o ID, horário ou hash da captura. O hash representa os bytes da matriz recebida; converter para PDF/A ou assinar cria outro artefato e exige outro hash. Para fluxo de órgãos públicos, habilitar `setorPublico: true` por configuração de projeto, não por checkbox livre.

Observação: esta biblioteca valida presença e formatos básicos, mas os controles normativos completos dependem de processos, assinaturas, tabelas, autenticação, armazenamento auditável e testes integrados.
