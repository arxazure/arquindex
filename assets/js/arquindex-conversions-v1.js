/* Arquindex conversion events v1. Safe opt-in; include on owned pages after QA.
   Requires an existing GA4 gtag installation. Never sends form values or PII. */
(function () {
  'use strict';
  var root = document.documentElement;
  if (root.dataset.arquindexConversions === '1') return;
  root.dataset.arquindexConversions = '1';
  function send(name, extra) {
    if (typeof window.gtag !== 'function') return;
    var payload = Object.assign({
      page_location: location.origin + location.pathname,
      page_path: location.pathname,
      event_source: 'arquindex_conversion_tracker_v1'
    }, extra || {});
    window.gtag('event', name, payload);
  }
  document.addEventListener('click', function (e) {
    var link = e.target.closest && e.target.closest('a[href]');
    if (!link) return;
    var href = link.getAttribute('href') || '';
    if (/^(https?:\/\/)?(wa\.me\/|api\.whatsapp\.com\/|web\.whatsapp\.com\/)/i.test(href)) {
      send('contact_whatsapp_click', {contact_method:'whatsapp'});
    } else if (/^tel:/i.test(href)) {
      send('contact_phone_click', {contact_method:'phone'});
    } else if (/^mailto:/i.test(href)) {
      send('contact_email_click', {contact_method:'email'});
    }
  }, {passive:true});
  /* Dispatch this event ONLY after a successful server-confirmed form submission:
     document.dispatchEvent(new CustomEvent('arquindex:lead-confirmed', {
       detail: {service: 'digitalizacao', form_id: 'orcamento'}
     }));
     No email, name, phone, document contents, or other PII may be passed. */
  document.addEventListener('arquindex:lead-confirmed', function (e) {
    var detail = e.detail || {};
    var safe = function(v) { return /^[a-z0-9_-]{1,60}$/i.test(String(v||'')) ? String(v) : 'unknown'; };
    send('generate_lead', {lead_service:safe(detail.service), form_id:safe(detail.form_id)});
  });
})();
