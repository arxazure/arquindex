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
