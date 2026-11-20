import * as fs from 'node:fs';
import * as path from 'node:path';
import { fileURLToPath } from 'node:url';

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const srcPath = path.join(__dirname, 'entry.png');
const outDir = process.env.MAKEFUN_OUTPUT_DIR || '/output';
const destPath = path.join(outDir, 'entry.png');

fs.mkdirSync(outDir, { recursive: true });
const buffer = fs.readFileSync(srcPath);
fs.writeFileSync(destPath, buffer);

const stats = fs.statSync(destPath);
console.log(`Output path: ${destPath}`);
console.log(`File size: ${stats.size} bytes`);
