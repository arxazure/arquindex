# LGPD Checklist — Arquindex Capture

Aplicação Express + PostgreSQL recuperada do pacote original e evoluída para implantação. O código não contém credenciais nem dados de clientes.

## Implantação

Railway: diretório `/lgpd-checklist`, `npm start`, healthcheck `/health`. Configure `DATABASE_URL` como referência ao serviço Postgres; `ADMIN_EMAIL`, `PUBLIC_ORIGIN` e `RUN_SELF_TESTS=true` são configurações não secretas. Migrações aditivas usam tabelas `lgpd_*` sem alterar tabelas anteriores. O teste no banco usa transação revertida e dados sintéticos.

No primeiro início, a administração recebe um link de ativação de uso único nos logs privados da implantação. O banco guarda somente o hash do token; o link vence em 24 horas. Não há senha padrão nem cadastro administrativo aberto ao público. Guarde o link no canal autorizado do proprietário. Usuários adicionais são convidados pela administração.

## Fluxos disponíveis

- Empresas, unidades, departamentos, agentes, sistemas, ROPA, riscos, incidentes, treinamentos, auditorias e varredura passiva e conferência manual de websites.
- CRUD com vínculo de empresa validado no servidor, perfis administrador, gestor por empresa e leitura por empresa; sessões seguras e CSRF.
- Políticas em rascunho a partir do cadastro e ROPA; publicação explícita pela administração. Edições retornam ao rascunho.
- Portal por empresa com versões publicadas, canal do titular e denúncias. Denúncias ficam restritas à administração. Protocolo e chave de acompanhamento; somente respostas marcadas públicas aparecem ao solicitante.
- Histórico de ações e exportação JSON por empresa.

## Limites explícitos

O módulo de websites permite varredura passiva autorizada de uma página HTTPS pública: cabeçalhos, atributos de Set-Cookie e sinais de privacidade no HTML. Salva histórico por empresa e inclui os relatórios na exportação. Bloqueia endereços internos e revalida redirecionamentos. Não executa JavaScript, navegação autenticada ou exploração de vulnerabilidades; consentimento e cookies no navegador exigem validação manual. Não há integração automática com ANPD, e-mail, cookies de sites externos ou faturamento. Planos comerciais são contratados mediante proposta. Rascunhos de políticas exigem revisão jurídica e aprovação. O sistema não substitui backup integral do PostgreSQL ou homologação operacional.

Validação: `npm test`; teste de segregação no PostgreSQL durante o início; testes HTTP sem autenticação após a implantação.
