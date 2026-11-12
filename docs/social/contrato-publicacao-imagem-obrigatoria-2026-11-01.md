# Integração obrigatória de imagens — Arquindex

## Objetivo
Impedir que LinkedIn, Instagram e Google Business recebam postagens apenas com texto.

## Contrato do publicador
1. Antes de reservar o item, verificar canal autorizado, texto e URL HTTPS de imagem em JPG/PNG/WEBP.
2. Validar a imagem remotamente: HTTP 200, Content-Type image/jpeg, image/png ou image/webp, conteúdo não vazio, dimensões e limites aceitos pelo canal. Não confiar somente na extensão da URL.
3. Se a mídia falhar, registrar `blocked_media` e **não chamar** create_image_post/create_local_post.
4. Depois da publicação, persistir ID remoto, horário, conta, URL da imagem, hash da mídia e resultado retornado pela plataforma.
5. Para status `accepted`, `unknown` ou `published`, consultar primeiro a plataforma por ID remoto. Nunca reenviar automaticamente sem reconciliação.
6. Google Business com `PROCESSING` não equivale a `LIVE`; verificar status final e presença da imagem.
7. Instagram: respeitar limite de postagens e permissões; nunca tentar compensar automaticamente um bloqueio por limite diário.
8. LinkedIn: usar publicação de imagem na organização correta e conferir mídia anexada no resultado.

## Auditoria da fila em 2026-11-01
Cinco registros anteriores tinham mídia ausente no campo local: LinkedIn (3) e Google Business (2). Como há IDs remotos, primeiro verificar posts existentes e corrigir a mídia neles quando a API permitir. Não recriar os posts.

## Critério de aceite
- Post novo sem imagem: bloqueado antes da chamada externa.
- Imagem com erro HTTP, MIME incorreto ou vazia: bloqueada.
- Post publicado: recibo remoto e mídia confirmados.
- Resultado desconhecido: sem duplicação.
- Evidência: logs e capturas dos três canais.

## Situação
O arquivo `scripts/validar-postagem-com-imagem.py` implementa somente a checagem estrutural local; seus testes passaram no workflow 41336270096. A validação HTTP, a integração ao publicador ativo e a conferência visual continuam pendentes. Este documento não ativa a regra em produção.
