# Arquindex Video AI — MVP

Protótipo isolado do site institucional, com Remotion e exportação de vídeo vertical 1080x1920, 30 fps, 15 segundos.

## Uso local

Requer Node.js LTS, npm e dependências de renderização do Remotion.

```bash
cd video-ai
npm install
npm run render:sample
```

O arquivo gerado será `out/arquindex-promo.mp4`. Este MVP **não** gera voz, legendas, imagens com IA ou publica em redes sociais. Essas integrações exigem módulos adicionais e testes. A marca exibida é texto provisório, não o logotipo oficial.

## Próximas etapas

1. Validar licença comercial do Remotion e dependências do FFmpeg.
2. Adicionar identidade visual oficial e biblioteca de mídia autorizada.
3. Integrar TTS em português brasileiro e Whisper para legendas.
4. Adicionar fila de renderização, armazenamento externo e controle de custos.
5. Construir aprovação humana e publicação via APIs autorizadas.

Não incluir segredos de APIs, tokens ou dados de clientes no repositório.

## Validação técnica

Veja [VALIDATION.md](VALIDATION.md) para evidências do MP4 existente, testes SRT/FFmpeg, limites e requisitos de integração/licença. Execute `python -m unittest discover -s tests -v` (Python 3.10+, FFmpeg e ffprobe com libass) e `python scripts/validate-video.py out/arquindex-promo.mp4`.

## Mídia local e legendas na composição

A composição aceita os parâmetros opcionais `logo` e `audio`, como caminhos relativos dentro de `video-ai/public/` (por exemplo `marca/logo.png` e `voz/narracao.wav`). Os arquivos devem ser autorizados e fornecidos separadamente; não existe download automático, serviço TTS ou cobrança. Não colocar dados sensíveis em public/.

`captions` recebe uma lista `{start, end, text}` em segundos: ordenada, sem sobreposição, duração positiva, dentro de 0–15 s. O fim de cada legenda é exclusivo. O texto é gravado na imagem pelo Remotion. O exemplo `sample-caption-props.json` tem tempos editoriais demonstrativos, sem voz: não representa alinhamento automático por Whisper.

```sh
npx remotion render src/index.ts ArquindexPromo out/arquindex-caption-demo.mp4 --props=sample-caption-props.json
```

Para adicionar uma voz real, use o roteiro demonstrativo como ponto de partida, confira se a gravação termina antes de 15 s e revise todos os tempos após ouvir o áudio. A composição limita a saída aos 15 s; áudio maior será cortado. O logotipo textual permanece enquanto não houver um arquivo oficial configurado. A área inferior reservada às legendas não garante margens corretas para textos arbitrariamente longos: revisar a prévia antes de aprovar.

### Verificação desta etapa

Em 04/11/2026, os testes SRT/FFmpeg e a checagem TypeScript passaram localmente. A renderização da nova composição foi tentada, mas o download do Chrome Headless foi bloqueado por timeout de rede neste ambiente. O workflow inclui a renderização e validação da demonstração com legendas para verificação no GitHub Actions. A prévia histórica validada não comprova esta nova composição.

Foi adicionado package-lock.json; o workflow usa npm ci para reproduzir a árvore instalada nesta etapa. O inventário de licenças transitivas ainda precisa ser concluído.
