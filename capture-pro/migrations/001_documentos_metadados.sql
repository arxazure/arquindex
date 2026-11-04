-- Capture Pro / PostgreSQL 16. Execute somente apos backup e revisao das roles.
-- app.capture_tenant precisa ser definido com SET LOCAL dentro de cada transacao autenticada.
CREATE SCHEMA IF NOT EXISTS capture_pro;
CREATE TABLE IF NOT EXISTS capture_pro.documentos (
 identificador_digital uuid PRIMARY KEY,
 tenant_id text NOT NULL CHECK (length(tenant_id)>0),
 projeto_id text NOT NULL,
 operador_id text NOT NULL,
 unidade_id text NOT NULL,
 criado_em timestamptz NOT NULL,
 local_digitalizacao text NOT NULL,
 responsavel_digitalizacao text NOT NULL,
 hash_matriz char(64) NOT NULL CHECK(hash_matriz ~ '^[0-9a-f]{64}$'),
 arquivo_matriz_chave text NOT NULL,
 assunto text,
 autor text,
 titulo text,
 tipo_documental text,
 dados_adicionais jsonb NOT NULL DEFAULT '{}'::jsonb,
 perfil_publico boolean NOT NULL DEFAULT false,
 estado text NOT NULL DEFAULT 'revisao' CHECK (estado IN ('revisao','validado','entregue')),
 revisado_por text,
 revisado_em timestamptz,
 versao integer NOT NULL DEFAULT 1 CHECK (versao>=1),
 CONSTRAINT documento_por_tenant UNIQUE(tenant_id,identificador_digital)
);
CREATE TABLE IF NOT EXISTS capture_pro.eventos (
 id bigint GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
 tenant_id text NOT NULL,
 identificador_digital uuid NOT NULL,
 instante timestamptz NOT NULL DEFAULT now(),
 ator_id text NOT NULL,
 acao text NOT NULL,
 detalhes jsonb NOT NULL DEFAULT '{}'::jsonb,
 FOREIGN KEY (tenant_id,identificador_digital) REFERENCES capture_pro.documentos(tenant_id,identificador_digital)
);
CREATE INDEX IF NOT EXISTS idx_capture_documentos_tenant_estado ON capture_pro.documentos(tenant_id,estado);
CREATE INDEX IF NOT EXISTS idx_capture_eventos_doc ON capture_pro.eventos(tenant_id,identificador_digital,instante);
CREATE OR REPLACE FUNCTION capture_pro.proteger_captura() RETURNS trigger LANGUAGE plpgsql AS $$
BEGIN
 IF OLD.identificador_digital IS DISTINCT FROM NEW.identificador_digital OR
    OLD.tenant_id IS DISTINCT FROM NEW.tenant_id OR
    OLD.criado_em IS DISTINCT FROM NEW.criado_em OR
    OLD.hash_matriz IS DISTINCT FROM NEW.hash_matriz OR
    OLD.arquivo_matriz_chave IS DISTINCT FROM NEW.arquivo_matriz_chave OR
    OLD.operador_id IS DISTINCT FROM NEW.operador_id OR
    OLD.local_digitalizacao IS DISTINCT FROM NEW.local_digitalizacao OR
    OLD.responsavel_digitalizacao IS DISTINCT FROM NEW.responsavel_digitalizacao
 THEN RAISE EXCEPTION 'Identidade, origem e hash da captura sao imutaveis'; END IF;
 IF NEW.versao <> OLD.versao+1 THEN RAISE EXCEPTION 'A versao deve incrementar em 1'; END IF;
 RETURN NEW;
END $$;
DROP TRIGGER IF EXISTS trg_proteger_captura ON capture_pro.documentos;
CREATE TRIGGER trg_proteger_captura BEFORE UPDATE ON capture_pro.documentos FOR EACH ROW EXECUTE FUNCTION capture_pro.proteger_captura();
CREATE OR REPLACE FUNCTION capture_pro.proteger_eventos() RETURNS trigger LANGUAGE plpgsql AS $$
BEGIN RAISE EXCEPTION 'Eventos de auditoria sao append-only'; END $$;
DROP TRIGGER IF EXISTS trg_proteger_eventos ON capture_pro.eventos;
CREATE TRIGGER trg_proteger_eventos BEFORE UPDATE OR DELETE ON capture_pro.eventos FOR EACH ROW EXECUTE FUNCTION capture_pro.proteger_eventos();
ALTER TABLE capture_pro.documentos ENABLE ROW LEVEL SECURITY;
ALTER TABLE capture_pro.documentos FORCE ROW LEVEL SECURITY;
ALTER TABLE capture_pro.eventos ENABLE ROW LEVEL SECURITY;
ALTER TABLE capture_pro.eventos FORCE ROW LEVEL SECURITY;
DROP POLICY IF EXISTS documentos_tenant ON capture_pro.documentos;
CREATE POLICY documentos_tenant ON capture_pro.documentos USING (tenant_id = current_setting('app.capture_tenant', true)) WITH CHECK (tenant_id = current_setting('app.capture_tenant', true));
DROP POLICY IF EXISTS eventos_tenant ON capture_pro.eventos;
CREATE POLICY eventos_tenant ON capture_pro.eventos USING (tenant_id = current_setting('app.capture_tenant', true)) WITH CHECK (tenant_id = current_setting('app.capture_tenant', true));
-- IMPORTANTE: role da aplicacao nao pode ser superuser nem ter BYPASSRLS;
-- impedir conexao da API usando role proprietaria de tabelas; nao aplicar automaticamente.
