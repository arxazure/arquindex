# Arquindex Capture Pro — módulo inicial de processamento

**Estado:** protótipo de código isolado, NÃO implantado. A branch não deve ser mesclada ou publicada sem testes e autorização.

## Dependência
Python 3.11+ e PyMuPDF (instalar em ambiente isolado): `pip install pymupdf`.

## Comandos de teste
```bash
python capture_pro/processing.py split --model prontuario --input exemplo_pesquisavel.pdf --out /tmp/revisao-prontuarios
python capture_pro/processing.py split --model dossie --input exemplo_pesquisavel.pdf --out /tmp/revisao-dossies
python capture_pro/processing.py backup --client cliente_teste --root /dados/cliente_teste --db /dados/cliente_teste.db --destination /backup-seguro
```

## Limitações e requisitos antes de produção

1. O processamento de separação usa **texto já extraível** dos PDFs. Falta integrar OCRmyPDF/Tesseract para os documentos digitalizados sem texto, preservando originais e criando versões pesquisáveis em PDF/A validadas.
2. A heurística de cabeçalho ainda é simples: não permite confirmar a identidade por CPF, matrícula, data de nascimento, variações de nome e layouts cadastrados. O resultado jamais deve ir automaticamente para assinatura ou entrega.
3. Não divide em páginas isoladas se o mesmo paciente continuar; porém, uma troca de nome em cabeçalho ou um nome ausente requer análise de qualidade. A fila de revisão é obrigatória.
4. Não há autenticação, política de autorização multiempresa nem consulta ao PostgreSQL de produção nesta versão. Nunca apontar a ferramenta para dados reais antes de desenvolver essas camadas.
5. O backup é **local, não criptografado**, e só produz um arquivo ZIP com dados do diretório autorizado e snapshot SQLite opcional. O destino precisa estar em disco cifrado e sujeito a controle de acesso. Não é backup completo do PostgreSQL, S3 ou da VM do Railway.
6. Um backup verdadeiro por cliente precisa consultar exclusivamente arquivos autorizados no S3, exportar metadados do PostgreSQL com filtros por tenant, gerar manifestos e testar restauração em ambiente separado.
7. Para backup do servidor físico/VM, integrar agente local com Proxmox, Hyper-V ou VMware, observando consistência dos volumes; Railway não expõe a imagem da VM gerenciada.
8. Para assinatura ICP-Brasil: integrar motor PAdES, cofre de chave privada, autorização por lote, cadeia de certificados, verificação de assinatura, hash de arquivo pré/pós assinatura e auditoria. Não salvar senha/certificado no GitHub.
9. Antes de entrar em produção: testes automatizados, testes com documentos reais anonimizados, comparação página a página, testes de segurança de isolamento entre clientes e de recuperação de backup.

## Fluxo-alvo
Digitalização/upload → OCR obrigatório → validação PDF/A → classificação e separação por modelo → revisão e aprovação humana → assinatura ICP-Brasil em lote → SHA-256 do PDF final → armazenamento S3 com auditoria → entrega ao cliente → backup por cliente e do ambiente.
