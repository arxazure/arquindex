function csvCell(value) {
  let s=value==null?'':value instanceof Date?value.toISOString().slice(0,10):String(value);
  if (/^[\s]*[=+@\-]/.test(s)) s="'"+s;
  return '"'+s.replace(/"/g,'""')+'"';
}
function csvDownload(res,basename,headers,rows){
  res.setHeader('Content-Type','text/csv; charset=utf-8');
  res.setHeader('Content-Disposition','attachment; filename="'+basename+'.csv"');
  res.setHeader('Cache-Control','private, no-store');
  res.send('\ufeff'+[headers,...rows].map(r=>r.map(csvCell).join(';')).join('\r\n'));
}
export function registerInventarioReports(app,db,wrap){
  app.get('/api/reports/inventario.csv',wrap(async(req,res)=>{
    const rows=await db.query(
      `SELECT b.code,b.department,b.doc_type,b.description,b.period_start,b.period_end,
       b.document_date,b.trigger_date,b.legal_hold,b.legal_hold_reason,s.name AS location,s.address
       FROM boxes b JOIN sites s ON s.id=b.site_id AND s.tenant_id=b.tenant_id
       WHERE b.tenant_id=$1 ORDER BY b.code LIMIT 50000`,[req.user.tenant_id]);
    const headers=['Etiqueta','Departamento','Tipo documental','Descrição','Período inicial',
      'Período final','Data do documento','Data do evento','Bloqueio legal',
      'Justificativa do bloqueio','Localização','Endereço'];
    csvDownload(res,'arquindex-inventario',headers,rows.rows.map(x=>[
      x.code,x.department,x.doc_type,x.description,x.period_start,x.period_end,
      x.document_date,x.trigger_date,x.legal_hold?'Sim':'Não',x.legal_hold_reason,x.location,x.address
    ]));
  }));
  app.get('/api/reports/temporalidade.csv',wrap(async(req,res)=>{
    const rows=await db.query(
      `SELECT b.code,b.doc_type,b.period_start,b.period_end,b.document_date,b.trigger_date,
         b.legal_hold,t.code AS type_code,t.current_years,t.intermediate_years,
         t.trigger_event,t.disposition,t.approved,t.legal_basis
       FROM boxes b LEFT JOIN document_types t ON t.tenant_id=b.tenant_id
         AND lower(t.name)=lower(b.doc_type)
       WHERE b.tenant_id=$1 ORDER BY b.code LIMIT 50000`,[req.user.tenant_id]);
    const headers=['Etiqueta','Tipo documental','Código documental','Período inicial',
      'Período final','Data documento','Data evento','Fase corrente (anos)',
      'Fase intermediária (anos)','Marco inicial','Destinação','Homologado',
      'Bloqueio legal','Fundamentação'];
    csvDownload(res,'arquindex-temporalidade',headers,rows.rows.map(x=>[
      x.code,x.doc_type,x.type_code,x.period_start,x.period_end,x.document_date,
      x.trigger_date,x.current_years,x.intermediate_years,x.trigger_event,x.disposition,
      x.approved?'Sim':'Não',x.legal_hold?'Sim':'Não',x.legal_basis
    ]));
  }));
}
