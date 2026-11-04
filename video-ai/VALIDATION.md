# Validação técnica — 04/11/2026

## Evidências

- PR #107 permanece rascunho; protótipo restrito a `video-ai/` e ao workflow próprio. Nenhum arquivo da aplicação institucional foi alterado.
- Head inspecionado: `c2a4c50c5f8aa533af21d7517b2ccd75961bb9d2`.
- Workflow Video AI preview: execução [41766812621](https://github.com/arxazure/arquindex/actions/runs/41766812621), conclusão success.
- Artefato `13292409449`, criado 04/11/2026 03:24:17 UTC, expira 11/11/2026 03:24:16 UTC. MP4 baixado desse artefato e validado, sem nova renderização ou serviço contratado.
- MP4 SHA-256: `b33fa2110fa372d966081755ad766572b26a6fd60caf7ca9289ad6c12f3a1eed`.
- H.264 High, yuv420p, 1080 × 1920, proporção 9:16, 30 fps, 450 quadros, 15,000 segundos, 188.419 bytes. Sem trilha de áudio ou legendas.
- FFmpeg decodificou o arquivo inteiro com `-xerror`, sem erros. Quadro de 5 segundos inspecionado: texto e acentos legíveis, sem cortes. Reprodução validada por decodificação; não foi realizado teste manual em aparelhos móveis ou redes sociais.

## Correções e testes

`generate-subtitles.py` agora grava quebras reais de linha e UTF-8, separa serialização de transcrição e carrega Whisper apenas quando solicitado. Rejeita tempos negativos, não finitos, duração nula após arredondamento para milissegundos, sobreposição, texto vazio e delimitador de tempo no texto. A validação ocorre antes de sobrescrever a saída. Whitespace interno é normalizado para não quebrar blocos SRT.

Três testes locais passaram, cobrindo múltiplos casos: estrutura exata e sequência dos blocos, acentos UTF-8, arredondamento e mudança de hora, tempos inválidos, sobreposição e entrada vazia; leitura de pacotes com ffprobe; conversão para mov_text em MP4; aplicação do filtro subtitles/libass em vídeo sintético.

O workflow agora executa esses testes e valida resolução, duração, fps, codec, formato de pixels, número de quadros e decodificação integral antes de disponibilizar o artefato. A execução histórica citada acima é anterior a essas alterações; não constitui evidência de execução dos novos passos.

Reproduzir:

```sh
cd video-ai
python -m unittest discover -s tests -v
python scripts/validate-video.py out/arquindex-promo.mp4
```

Whisper real não foi instalado nem executado: os testes usam segmentos sintéticos e não comprovam qualidade de transcrição/sincronismo de uma voz real. A sincronização final deve ser revisada após existir a narração.

## Componentes adicionais

1. Logotipo oficial autorizado em SVG ou PNG transparente, identidade visual e direitos das fontes/mídias; colocar o arquivo em `public/`, usar `staticFile`/`Img` do Remotion, preservar proporção e margens seguras. O texto ARQUINDEX atual continua provisório.
2. Roteiro aprovado e voz pt-BR: gravação humana autorizada ou motor TTS com licença comercial e licença específica da voz/modelo verificadas. Não há fornecedor selecionado, conta criada, clonagem de voz ou cobrança autorizada. Medir o áudio e ajustar roteiro/timeline aos 15 segundos; integrar com componente Audio e codificar AAC.
3. Transcrição local Whisper com modelo versionado e timestamps, seguida de revisão humana; gerar SRT com o escritor corrigido. Aplicar libass/FFmpeg para legendas gravadas na imagem (mais previsíveis em redes sociais), ou mov_text para uma trilha selecionável. Conferir limites da timeline e sincronismo no áudio final.
4. Fixar versões/lockfile, inventariar dependências transitivas e binários Chromium/FFmpeg, fontes e modelos antes de operação comercial. O package.json atual usa intervalos e a prévia identifica Remotion 4.0.540; não há lockfile que permita reproduzir exatamente a árvore histórica.

## Licenças verificadas e limites

Fontes oficiais consultadas em 04/11/2026:

| Componente | Requisito |
| --- | --- |
| Remotion/CLI | Licença própria. Avaliação sem uso comercial é elegível à licença gratuita. Para uso comercial, organizações com até 3 empregados podem ser elegíveis; organizações com 4 ou mais precisam de Company License. Confirmar enquadramento da Arquindex e modalidade antes da operação comercial. Não é MIT. |
| React/React DOM | MIT; preservar avisos ao redistribuir software. |
| TypeScript | Apache-2.0; preservar licença/avisos aplicáveis ao redistribuir. Ferramenta de desenvolvimento. |
| Whisper opcional | Código sob MIT; preservar avisos e verificar também os pesos/modelos e dependências efetivamente escolhidos. Não é um gerador de voz. |
| FFmpeg | LGPL por padrão, com componentes opcionais GPL. Os scripts usam libx264: o binário correspondente envolve GPL; redistribuição exige cumprir as condições aplicáveis. Patentes de codecs são uma questão separada. |
| TTS, voz, logo, fontes, música e imagens | Não cobertos automaticamente pelas licenças acima; seleção e autorização ainda pendentes. |

Referências:
- https://github.com/remotion-dev/remotion/blob/main/packages/core/LICENSE.md
- https://www.remotion.dev/docs/license/pricing
- https://github.com/react/react/blob/main/LICENSE
- https://github.com/microsoft/TypeScript/blob/main/LICENSE.txt
- https://github.com/openai/whisper/blob/main/LICENSE
- https://ffmpeg.org/legal.html
- https://github.com/FFmpeg/FFmpeg/blob/master/LICENSE.md

Esta revisão cobre os componentes diretos identificados; não equivale a uma auditoria concluída de todos os pacotes transitivos ou a liberação comercial definitiva.

## Aprovação futura

Nenhuma mesclagem, publicação social ou ativação de serviço pago foi feita. Antes dessas ações, apresentar escopo, canais, vídeo final, enquadramento/licença e eventuais custos para aprovação expressa. O PR continua rascunho. O estado de mesclagem pode ser recalculado pelo GitHub; nenhuma atualização da base institucional foi incorporada neste trabalho.
