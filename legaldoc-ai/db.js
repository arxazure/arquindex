import pg from 'pg';
export const pool=new pg.Pool({connectionString:process.env.DATABASE_URL,max:6,connectionTimeoutMillis:7000,idleTimeoutMillis:20000,ssl:process.env.PGSSL==='require'?{rejectUnauthorized:true}:undefined});
export async function initDb(){
 await pool.query(`
 CREATE TABLE IF NOT EXISTS ld_tenants(
 id uuid PRIMARY KEY,name varchar(180) NOT NULL,created_at timestamptz NOT NULL DEFAULT now());
 CREATE TABLE IF NOT EXISTS ld_users(
 id uuid PRIMARY KEY,tenant_id uuid NOT NULL REFERENCES ld_tenants(id),email varchar(254) NOT NULL,
 password_hash text NOT NULL,role varchar(20) NOT NULL CHECK(role IN ('admin','author','client','legal','technical','approver','homologator')),
 active boolean NOT NULL DEFAULT true,created_at timestamptz NOT NULL DEFAULT now(), UNIQUE(tenant_id,email));
 CREATE TABLE IF NOT EXISTS ld_sessions(
 token_hash char(64) PRIMARY KEY,user_id uuid NOT NULL REFERENCES ld_users(id),
 csrf_hash char(64) NOT NULL,expires_at timestamptz NOT NULL,created_at timestamptz NOT NULL DEFAULT now());
 CREATE INDEX IF NOT EXISTS ld_sessions_expiry ON ld_sessions(expires_at);
 CREATE TABLE IF NOT EXISTS ld_documents(
 id uuid PRIMARY KEY,tenant_id uuid NOT NULL REFERENCES ld_tenants(id),created_by uuid NOT NULL REFERENCES ld_users(id),
 title varchar(180) NOT NULL,doc_type varchar(180) NOT NULL,request_text text NOT NULL,
 review_rounds smallint NOT NULL CHECK(review_rounds IN(1,2)),legal_emails jsonb NOT NULL,
 outcome varchar(10) NOT NULL CHECK(outcome IN('PUBLISH','SIGN')),
 workflow_stages jsonb NOT NULL,stage_index smallint NOT NULL DEFAULT 1,
 revision_cycle integer NOT NULL DEFAULT 1,version integer NOT NULL DEFAULT 1,
 state varchar(40) NOT NULL DEFAULT 'DRAFT',updated_at timestamptz NOT NULL DEFAULT now(),
 created_at timestamptz NOT NULL DEFAULT now());
 CREATE INDEX IF NOT EXISTS ld_documents_tenant ON ld_documents(tenant_id,updated_at DESC);
 CREATE TABLE IF NOT EXISTS ld_versions(
 id uuid PRIMARY KEY,tenant_id uuid NOT NULL,document_id uuid NOT NULL REFERENCES ld_documents(id),
 version integer NOT NULL,body text NOT NULL,content_hash char(64) NOT NULL,
 created_by uuid NOT NULL REFERENCES ld_users(id),created_at timestamptz NOT NULL DEFAULT now(),
 UNIQUE(document_id,version));
 CREATE INDEX IF NOT EXISTS ld_versions_tenant ON ld_versions(tenant_id,document_id,version DESC);
 CREATE TABLE IF NOT EXISTS ld_decisions(
 id uuid PRIMARY KEY,tenant_id uuid NOT NULL,document_id uuid NOT NULL REFERENCES ld_documents(id),
 stage varchar(50) NOT NULL,revision_cycle integer NOT NULL,actor_id uuid NOT NULL REFERENCES ld_users(id),
 outcome varchar(16) NOT NULL CHECK(outcome IN('APPROVE','CHANGES')),
 note text NOT NULL,document_hash char(64) NOT NULL,created_at timestamptz NOT NULL DEFAULT now());
 CREATE INDEX IF NOT EXISTS ld_decisions_tenant ON ld_decisions(tenant_id,document_id,revision_cycle);
 CREATE TABLE IF NOT EXISTS ld_events(
 id uuid PRIMARY KEY,tenant_id uuid NOT NULL,document_id uuid NOT NULL REFERENCES ld_documents(id),
 actor_id uuid NOT NULL REFERENCES ld_users(id),kind varchar(50) NOT NULL,
 detail jsonb NOT NULL DEFAULT '{}'::jsonb,created_at timestamptz NOT NULL DEFAULT now());
 CREATE INDEX IF NOT EXISTS ld_events_tenant ON ld_events(tenant_id,document_id,created_at);
 `);
}
