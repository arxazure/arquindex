# Rodada SEO/GEO/AEO — ARQ-185 a ARQ-190 — 06/11/2026 (noite)

## Escopo e evidências

- Auditoria técnica: [workflow 42313999728](https://github.com/arxazure/arquindex/actions/runs/42313999728), commit `797b00847f0b3306e59f8f073a0d8635acedf17c`, conclusão **success**.
- Publicação de identidade: [workflow 42314917021](https://github.com/arxazure/arquindex/actions/runs/42314917021), commit `cae51f24622b6ce8f5f0da2cd0c4a27f3d09016a`, conclusão **success**.
- Limites respeitados: seis URLs auditadas e três melhorias publicadas.
- ARQ-099 não foi alterada nem republicada.

## Auditoria

| ID | Situação pública verificada | Diagnóstico principal |
|---|---|---|
| ARQ-185 | DNS/SSL válidos, HTTP 200, canonical próprio, indexável, robots e sitemap 200 | identidade oficial ausente e overflow móvel 512/390 |
| ARQ-186 | DNS/SSL válidos, HTTP 200, canonical próprio, indexável | identidade ausente, overflow móvel e sitemap sem a própria URL |
| ARQ-187 | DNS/SSL válidos, HTTP 200, canonical próprio, indexável, sitemap contém URL | identidade ausente e overflow móvel; intenção próxima de ARQ-186 |
| ARQ-188 | DNS/SSL válidos, HTTP 200, indexável, sem overflow | canonical aponta para `www.arquindex.com.br/output/...`, conteúdo raso (305 palavras), sem WhatsApp e identidade oficial |
| ARQ-189 | DNS/SSL válidos, HTTP 200, canonical próprio, indexável | title/H1 tratam gestão documental em vez da intenção LGPD, overflow e sitemap sem URL |
| ARQ-190 | DNS/SSL válidos, HTTP 200, canonical próprio, indexável | title/H1 ainda genéricos para gestão da informação, identidade ausente, overflow e sitemap sem URL |

Todas as seis páginas responderam com exatamente um H1, meta description, viewport, JSON-LD e links internos. Nenhuma tinha formulário ou CTA com UTM no momento da auditoria.

## Melhorias publicadas e verificadas

### ARQ-185
- URL: https://empresas-digitalizacao-documentos-regiao.arquindex.com.br/
- Alteração: identidade oficial, cabeçalho/menu responsivo, rodapé e WhatsApp flutuante; correção do overflow móvel sem alterar title, H1, description ou canonical.
- Teste público: HTTP 200; canonical próprio; index,follow; logo/menu/WhatsApp/marcador presentes; mobile 390/390 e desktop 1440/1440.
- Backup: `/seo-backups/identidade-20261106T235505Z/a3e2398f2a907afbe824.html`
- SHA-256: `859abfee13d233bfe8635603658a846a946ada0c92785f64db7f0532eb0dbd33`
- Descoberta: robots.txt 200 e sitemap.xml 200 contendo a URL.

### ARQ-186
- URL: https://essenciais-oferecidos-por-consultoria-lgpd.arquindex.com.br/
- Alteração: identidade oficial e correção responsiva, preservando conteúdo e metadados.
- Teste público: HTTP 200; canonical próprio; index,follow; identidade e WhatsApp presentes; mobile 390/390 e desktop 1440/1440.
- Backup: `/seo-backups/identidade-20261106T235525Z/6f55f54fa8906121b2d4.html`
- SHA-256: `ca1a0def66f1fb0597445899c659613b84a32e2873be18695d453f7b5fc70eb2`
- Descoberta: robots.txt e sitemap.xml 200; sitemap ainda não contém a URL.

### ARQ-190
- URL: https://ia.arquindex.com.br/
- Alteração: identidade oficial e correção responsiva, sem transformar a página em alegação de serviço de IA não comprovado.
- Teste público: HTTP 200; canonical próprio; index,follow; identidade e WhatsApp presentes; mobile 390/390 e desktop 1440/1440.
- Backup: `/seo-backups/identidade-20261106T235543Z/9a6046ff1f2512fdabcd.html`
- SHA-256: `e5568dec4c09fdaad1af264289b5104482070abfad4e75b83d1501ebafeb3c20`
- Descoberta: robots.txt e sitemap.xml 200; sitemap ainda não contém a URL.

## Pendências priorizadas

1. ARQ-188: corrigir canonical e aprofundar a diferença entre organização da informação, GED e ECM antes de promover.
2. ARQ-189: resolver o desalinhamento entre a URL LGPD e o conteúdo de gestão documental antes de qualquer divulgação.
3. ARQ-186 e ARQ-190: incluir no sitemap correspondente após confirmar a origem geradora do XML; não houve nova URL nesta rodada e não foi feita submissão redundante.
4. ARQ-187: diferenciar intenção e conteúdo de ARQ-186 antes de padronizar identidade ou divulgar.
5. CTAs com UTM e formulários devem ser tratados somente após confirmar o destino e o evento de lead; nenhum lead ou posição foi inferido.
6. Não houve divulgação social nesta rodada, evitando duplicação com a rotina social. Não houve envio ao Search Console, Bing ou IndexNow.
