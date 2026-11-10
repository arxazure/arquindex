# Capture Pro — índice probabilístico (POC sintética)
Implementação independente, sem API tranSkriptorium, sem cópia do PrIx e sem chamadas de rede.
Arquivo: `capture-pro/probabilistic/index.js`. Testes: `node --test capture-pro/probabilistic/index.test.js`.
## Implementado
- Hipóteses alternativas por token com probabilidades normalizadas, coordenadas e hash da imagem.
- Busca lexical por soma das probabilidades das hipóteses exatas; busca vetorial por cosseno sobre embeddings fornecidos localmente e filtrados por tenant.
- Extração simples por expressões regulares sobre transcrição top-1, sempre marcada para revisão humana.
- Correção revisada imutável, com incremento de revisão; envelope de metadados Alfresco sem transporte.
- Bloqueio de documentos não marcados sintéticos.
## Ainda não implementado
OCR/HTR real, geração de embeddings, indexação persistente, pesquisa em escala, interface de revisão, autenticação real, publicação Alfresco, exportação ALTO/PAGE XML, integrações OpenArch, treinamento ou calibração probabilística.
A marcação `synthetic:true` é apenas uma barreira de laboratório, **não é verificação de origem confiável**. Não conectar a API pública nem ativar em produção. Requer verificação server-side, ACL/RLS, consentimento, métricas, testes de integração e revisão de segurança antes de qualquer deploy.
Não alterar o adaptador OpenArch 0.2.1 nem sua flag. Não há integração remota.
