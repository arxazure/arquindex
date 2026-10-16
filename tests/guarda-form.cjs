const { chromium } = require('playwright');
const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('node:path');
const root = path.resolve(__dirname, '..');
const source = 'seo-regional/56-sites/guardadocumentalembh.arquindex.com.br/index.html';
(async () => {
  assert.equal(fs.readFileSync(path.join(root, source), 'utf8'), fs.readFileSync(path.join(root, 'deploy/subdominios/guardadocumentalembh/index.html'), 'utf8'));
  assert.ok(fs.readFileSync(path.join(root, source), 'utf8').includes(fs.readFileSync(path.join(root, 'scripts/templates/guarda-commercial-form.html'), 'utf8').trim()), 'Published form matches its template');
  const browser = await chromium.launch({headless:true, args:['--no-sandbox']});
  try {
    for (const width of [360, 390, 1280]) {
      const context = await browser.newContext({viewport:{width,height:900}});
      const page = await context.newPage();
      const errors = []; page.on('pageerror', error => errors.push(String(error)));
      let outbound;
      await page.route('https://wa.me/**', async route => {outbound = route.request().url(); await route.fulfill({status:200,body:'WhatsApp intercepted; no message sent.'});});
      await page.goto('file://' + path.join(root, source));
      assert.equal(await page.locator('#commercial-form').isVisible(), true);
      assert.equal(await page.locator('#storage-details').isVisible(), false);
      assert.equal(await page.evaluate(() => document.documentElement.scrollWidth <= innerWidth), true, 'No horizontal overflow');
      // Required fields and no service selection must prevent navigation.
      await page.locator('button[type=submit]').click(); assert.equal(outbound, undefined);
      await page.locator('#lead-name').fill('Marina Teste');
      await page.locator('#lead-company').fill('Empresa & Teste');
      await page.locator('#lead-email').fill('comercial@example.com');
      await page.locator('#lead-phone').fill('(31) 97363-2725');
      await page.locator('#lead-ack').check();
      await page.locator('button[type=submit]').click(); assert.equal(outbound, undefined);
      await page.locator('#service-storage').check();
      assert.equal(await page.locator('#storage-details').isVisible(), true);
      assert.equal(await page.locator('#service-storage').getAttribute('aria-expanded'), 'true');
      for (const value of ['Digitalização','OCR','Gestão documental','Descarte seguro','LGPD','Alfresco']) await page.locator(`[name="servicos"][value="${value}"]`).check();
      await page.locator('#storage-boxes').fill('-1');
      await page.locator('button[type=submit]').click(); assert.equal(outbound, undefined);
      await page.locator('#storage-boxes').fill('250');
      await page.locator('#storage-location').fill('Belo Horizonte / MG — Centro');
      await page.locator('#storage-collection').selectOption({label:'Sim'});
      await page.locator('#storage-access').selectOption({label:'Semanal'});
      await page.locator('#storage-scan').selectOption({label:'Quero conhecer'});
      await page.locator('[name=relacionados]').first().check();
      await page.locator('#lead-notes').fill('Prazo: 30 dias & OCR + indexação');
      await page.locator('#lead-phone').fill('abc123');
      await page.locator('button[type=submit]').click(); assert.equal(outbound, undefined);
      await page.locator('#lead-phone').fill('+55 31 97363-2725');
      await page.locator('#lead-email').fill('invalido');
      await page.locator('button[type=submit]').click(); assert.equal(outbound, undefined);
      await page.locator('#lead-email').fill('comercial@example.com');
      await page.locator('#lead-ack').uncheck();
      await page.locator('button[type=submit]').click(); assert.equal(outbound, undefined);
      await page.locator('#lead-ack').check();
      if (process.env.SCREENSHOT_DIR) {
        fs.mkdirSync(process.env.SCREENSHOT_DIR, {recursive:true});
        await page.locator('#orcamento').screenshot({path:path.join(process.env.SCREENSHOT_DIR, `guarda-${width}.png`)});
      }
      assert.equal(await page.locator('#commercial-form input, #commercial-form select, #commercial-form textarea').evaluateAll(elements => elements.every(el => el.labels.length > 0)), true, 'Every field has a label');
      // Keyboard focus and labels remain usable.
      await page.locator('#storage-scan').focus(); await page.keyboard.press('Tab');
      assert.equal(await page.locator('[name=relacionados]').first().evaluate(el => el === document.activeElement), true);
      await page.locator('button[type=submit]').click();
      await page.waitForURL('https://wa.me/**');
      const message = new URL(outbound).searchParams.get('text');
      for (const text of ['Marina Teste','Empresa & Teste','comercial@example.com','Caixas: 250','Localização: Belo Horizonte / MG — Centro','Consultas: Semanal','Inventário e etiquetagem','30 dias & OCR + indexação','Digitalização, OCR, Gestão documental, Guarda física, Descarte seguro, LGPD, Alfresco']) assert.ok(message.includes(text), text);
      assert.equal(new URL(outbound).pathname, '/5531973632725');
      await page.goto('file://' + path.join(root, source)); outbound = undefined;
      await page.locator('#service-storage').check(); await page.locator('#storage-location').fill('DADO OCULTO'); await page.locator('#service-storage').uncheck();
      assert.equal(await page.locator('#storage-details').isVisible(), false);
      await page.locator('#lead-name').fill('  '); await page.locator('#lead-company').fill('Empresa'); await page.locator('#lead-email').fill('a@example.com'); await page.locator('#lead-phone').fill('31999999999'); await page.locator('[value=OCR]').check(); await page.locator('#lead-ack').check();
      await page.locator('button[type=submit]').click(); assert.equal(outbound, undefined);
      await page.locator('#lead-name').fill('Cliente');
      await page.locator('button[type=submit]').click(); await page.waitForURL('https://wa.me/**');
      assert.ok(!new URL(outbound).searchParams.get('text').includes('DADO OCULTO'));
      assert.ok(!new URL(outbound).searchParams.get('text').includes('GUARDA DOCUMENTAL'));
      assert.deepEqual(errors, []);
      console.log(`PASS ${width}px: validation, multi-service, conditional fields, keyboard, WhatsApp encoding, no hidden data`);
      await context.close();
    }
    const context = await browser.newContext({javaScriptEnabled:false}); const page = await context.newPage();
    await page.goto('file://' + path.join(root, source));
    assert.equal(await page.locator('noscript a').isVisible(),true); assert.equal(await page.locator('#commercial-form').isVisible(),false);
    await context.close(); console.log('PASS no-JavaScript fallback and identical publication copies');
  } finally {await browser.close();}
})().catch(error => {console.error(error);process.exit(1);});
