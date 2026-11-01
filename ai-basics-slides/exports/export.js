const fs = require('fs');
const path = require('path');
const puppeteer = require('puppeteer');

(async () => {
  const outDir = __dirname;
  const excalidrawPath = path.resolve(__dirname, '../ai-basics-slides.excalidraw');
  const htmlPath = path.join(outDir, 'export_runner.html');

  const raw = fs.readFileSync(excalidrawPath, 'utf8');
  const doc = JSON.parse(raw);

  const frames = doc.elements.filter(e => e.type === 'frame');
  console.log(`Found ${frames.length} frames.`);

  const browser = await puppeteer.launch({
    headless: 'new',
    executablePath: '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome',
    args: ['--no-sandbox', '--disable-setuid-sandbox', '--allow-file-access-from-files']
  });

  const page = await browser.newPage();
  await page.setViewport({ width: 1920, height: 1080 });

  console.log('Loading runner page...');
  await page.goto(`file://${htmlPath}`, { waitUntil: 'load', timeout: 30000 });
  await page.waitForFunction(() => window.__READY__ === true);
  console.log('Excalidraw module ready.');

  for (let i = 0; i < frames.length; i++) {
    const frame = frames[i];
    console.log(`Processing Slide ${i + 1}: ${frame.name}...`);

    // Get elements for this frame
    const frameElements = doc.elements.filter(e => e.frameId === frame.id || e.id === frame.id);

    // Normalize coordinates so frame top-left is at (0, 0)
    const normalizedElements = frameElements.map(e => {
      const copy = JSON.parse(JSON.stringify(e));
      copy.x = copy.x - frame.x;
      copy.y = copy.y - frame.y;
      return copy;
    });

    const svgString = await page.evaluate(async (elements) => {
      const { exportToSvg } = window.ExcalidrawLib;
      const svg = await exportToSvg({
        elements: elements,
        appState: {
          viewBackgroundColor: "#FFFFFF",
          exportWithDarkMode: false,
          exportBackground: true,
          exportScale: 2
        },
        files: {}
      });
      return svg.outerHTML;
    }, normalizedElements);

    const svgPath = path.join(outDir, `slide_0${i + 1}.svg`);
    fs.writeFileSync(svgPath, svgString, 'utf8');

    // Convert SVG to PNG using a clean page
    const renderPage = await browser.newPage();
    await renderPage.setViewport({ width: 1600 * 2, height: 900 * 2, deviceScaleFactor: 1 });
    await renderPage.setContent(`
      <!DOCTYPE html>
      <html>
      <head>
        <style>
          * { margin: 0; padding: 0; box-sizing: border-box; }
          body { background: white; display: flex; align-items: center; justify-content: center; width: 100vw; height: 100vh; overflow: hidden; }
          svg { width: 100%; height: 100%; }
        </style>
      </head>
      <body>
        ${svgString}
      </body>
      </html>
    `, { waitUntil: 'networkidle0' });

    const pngPath = path.join(outDir, `slide_0${i + 1}.png`);
    const svgEl = await renderPage.$('svg');
    if (svgEl) {
      await svgEl.screenshot({ path: pngPath, type: 'png' });
    } else {
      await renderPage.screenshot({ path: pngPath, type: 'png' });
    }
    await renderPage.close();
    console.log(`✅ Saved PNG: ${pngPath}`);
  }

  await browser.close();
  console.log('🎉 All 6 slides successfully exported to PNG!');
})();
