const fs = require('fs');
const path = require('path');
const puppeteer = require('puppeteer');

(async () => {
  const excalidrawPath = '/Users/daipeng/Workspace/excalidraw-ppt/workbuddy-cloud-slides/workbuddy-cloud-slides.excalidraw';
  const outDir = '/Users/daipeng/Workspace/excalidraw-ppt/workbuddy-cloud-slides/exports';
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

    const frameElements = doc.elements.filter(e => e.frameId === frame.id || e.id === frame.id);

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

    const slideNum = (i + 1 < 10 ? `0${i + 1}` : `${i + 1}`);
    const svgPath = path.join(outDir, `slide_${slideNum}.svg`);
    fs.writeFileSync(svgPath, svgString, 'utf8');

    // Render SVG into PNG via browser using standard system fonts
    const renderPage = await browser.newPage();
    await renderPage.setViewport({ width: 1600, height: 900, deviceScaleFactor: 2 });
    await renderPage.setContent(`
      <!DOCTYPE html>
      <html>
        <head>
          <style>
            * { margin: 0; padding: 0; box-sizing: border-box; font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", "PingFang SC", "Hiragino Sans GB", "Microsoft YaHei", sans-serif; }
            body { background: #ffffff; display: flex; align-items: center; justify-content: center; width: 1600px; height: 900px; overflow: hidden; }
            svg { width: 1600px; height: 900px; }
          </style>
        </head>
        <body>
          ${svgString}
        </body>
      </html>
    `, { waitUntil: 'networkidle0' });

    const pngPath = path.join(outDir, `slide_${slideNum}.png`);
    await renderPage.screenshot({ path: pngPath, type: 'png' });
    await renderPage.close();

    console.log(` Saved slide_${slideNum}.svg and slide_${slideNum}.png with clear standard font!`);
  }

  await browser.close();
  console.log(' All slides successfully exported!');
})();
