/**
 * PPTX Converter - Converts HTML slides to PowerPoint format
 *
 * Usage: node convert.js <input.json> <output.pptx>
 */

import pptxgen from 'pptxgenjs';
import fs from 'fs';

// Parse command line arguments
const args = process.argv.slice(2);
if (args.length < 2) {
  console.error('Usage: node convert.js <input.json> <output.pptx>');
  process.exit(1);
}

const inputPath = args[0];
const outputPath = args[1];

// Read input JSON
let inputData;
try {
  const inputContent = fs.readFileSync(inputPath, 'utf-8');
  inputData = JSON.parse(inputContent);
} catch (error) {
  console.error(`Error reading input file: ${error.message}`);
  process.exit(1);
}

// Create presentation
const pptx = new pptxgen();
pptx.title = inputData.title || 'Untitled Presentation';
pptx.author = 'AI Presentation Generator';

// Set slide dimensions (16:9)
pptx.defineLayout({ name: 'CUSTOM', width: 10, height: 5.625 });
pptx.layout = 'CUSTOM';

// Theme settings
const theme = inputData.theme || {};
const defaultPrimaryColor = normalizeColor(theme.primaryColor) || '1a73e8';
const fontFamily = theme.fontFamily || 'Arial';

/**
 * Normalize color to 6-char hex without #
 */
function normalizeColor(color) {
  if (!color) return null;
  color = color.replace('#', '').trim();
  if (color.length === 3) {
    color = color[0] + color[0] + color[1] + color[1] + color[2] + color[2];
  }
  return color.toUpperCase();
}

/**
 * Convert RGB to hex
 */
function rgbToHex(r, g, b) {
  return ((1 << 24) + (r << 16) + (g << 8) + b).toString(16).slice(1).toUpperCase();
}

/**
 * Parse color from CSS value (hex, rgb, rgba)
 */
function parseColor(colorStr) {
  if (!colorStr) return null;

  // Hex color
  const hexMatch = colorStr.match(/#([0-9a-fA-F]{3,6})/);
  if (hexMatch) {
    return normalizeColor(hexMatch[1]);
  }

  // RGB/RGBA
  const rgbMatch = colorStr.match(/rgba?\s*\(\s*(\d+)\s*,\s*(\d+)\s*,\s*(\d+)/);
  if (rgbMatch) {
    return rgbToHex(parseInt(rgbMatch[1]), parseInt(rgbMatch[2]), parseInt(rgbMatch[3]));
  }

  // Named colors
  const namedColors = {
    white: 'FFFFFF', black: '000000', red: 'FF0000', green: '008000',
    blue: '0000FF', yellow: 'FFFF00', gray: '808080', grey: '808080'
  };
  const lower = colorStr.toLowerCase().trim();
  if (namedColors[lower]) return namedColors[lower];

  return null;
}

/**
 * Check if color is light
 */
function isLightColor(hex) {
  if (!hex) return true;
  hex = hex.replace('#', '');
  const r = parseInt(hex.substr(0, 2), 16);
  const g = parseInt(hex.substr(2, 2), 16);
  const b = parseInt(hex.substr(4, 2), 16);
  return (r * 299 + g * 587 + b * 114) / 1000 > 128;
}

/**
 * Extract styles from style attribute string
 */
function parseStyleAttr(styleStr) {
  const styles = {};
  if (!styleStr) return styles;

  const declarations = styleStr.split(';');
  for (const decl of declarations) {
    const colonIdx = decl.indexOf(':');
    if (colonIdx > 0) {
      const prop = decl.slice(0, colonIdx).trim().toLowerCase();
      const value = decl.slice(colonIdx + 1).trim();
      styles[prop] = value;
    }
  }
  return styles;
}

/**
 * Extract background from root div
 */
function extractBackground(html) {
  const divMatch = html.match(/<div[^>]*style="([^"]*)"/i);
  if (!divMatch) return null;

  const styles = parseStyleAttr(divMatch[1]);
  const bgValue = styles['background'] || styles['background-color'];
  if (!bgValue) return null;

  // Check for gradient
  const gradientMatch = bgValue.match(/linear-gradient\s*\([^)]+\)/i);
  if (gradientMatch) {
    // Extract all colors from gradient
    const colors = [];
    const hexMatches = bgValue.matchAll(/#([0-9a-fA-F]{3,6})/g);
    for (const m of hexMatches) colors.push(normalizeColor(m[1]));

    const rgbMatches = bgValue.matchAll(/rgba?\s*\(\s*(\d+)\s*,\s*(\d+)\s*,\s*(\d+)/g);
    for (const m of rgbMatches) colors.push(rgbToHex(parseInt(m[1]), parseInt(m[2]), parseInt(m[3])));

    if (colors.length > 0) {
      return { type: 'gradient', colors };
    }
  }

  // Solid color
  const color = parseColor(bgValue);
  if (color) {
    return { type: 'solid', color };
  }

  return null;
}

/**
 * Parse an HTML element and extract text with styling
 */
function parseElement(html, tagName) {
  const regex = new RegExp(`<${tagName}[^>]*(?:style="([^"]*)")?[^>]*>([\\s\\S]*?)<\\/${tagName}>`, 'gi');
  const elements = [];

  let match;
  while ((match = regex.exec(html)) !== null) {
    const fullTag = match[0];
    const content = match[2];

    // Extract style from the full tag (regex group might miss it)
    const styleMatch = fullTag.match(/style="([^"]*)"/i);
    const styles = styleMatch ? parseStyleAttr(styleMatch[1]) : {};

    elements.push({
      text: stripHtml(content),
      styles
    });
  }

  return elements;
}

/**
 * Strip HTML tags and decode entities
 */
function stripHtml(html) {
  return html
    .replace(/<[^>]*>/g, '')
    .replace(/&nbsp;/g, ' ')
    .replace(/&amp;/g, '&')
    .replace(/&lt;/g, '<')
    .replace(/&gt;/g, '>')
    .replace(/&quot;/g, '"')
    .replace(/&#39;/g, "'")
    .trim();
}

/**
 * Detect if slide has centered layout (flexbox centering)
 */
function hasCenteredLayout(html) {
  const styleMatch = html.match(/<div[^>]*style="([^"]*)"/i);
  if (!styleMatch) return false;

  const styles = parseStyleAttr(styleMatch[1]);
  return (
    styles['display'] === 'flex' ||
    styles['justify-content'] === 'center' ||
    styles['align-items'] === 'center' ||
    styles['text-align'] === 'center'
  );
}

/**
 * Get text alignment from styles
 */
function getAlignment(styles) {
  const align = styles['text-align'];
  if (align === 'center') return 'center';
  if (align === 'right') return 'right';
  return 'left';
}

// Process each slide
for (const slideData of inputData.slides || []) {
  const slide = pptx.addSlide();
  const html = slideData.html || '';

  // Extract and apply background
  const bg = extractBackground(html);
  let isDarkBg = false;

  if (bg) {
    if (bg.type === 'gradient' && bg.colors.length >= 2) {
      // Use first color for solid approximation
      slide.background = { color: bg.colors[0] };
      isDarkBg = !isLightColor(bg.colors[0]);
    } else if (bg.type === 'solid') {
      slide.background = { color: bg.color };
      isDarkBg = !isLightColor(bg.color);
    }
  }

  // Detect layout
  const isCentered = hasCenteredLayout(html);

  // Parse elements
  const h1s = parseElement(html, 'h1');
  const h2s = parseElement(html, 'h2');
  const ps = parseElement(html, 'p');
  const uls = html.matchAll(/<ul[^>]*>([\s\S]*?)<\/ul>/gi);

  // Determine default text color based on background
  const defaultTextColor = isDarkBg ? 'FFFFFF' : '333333';
  const defaultTitleColor = isDarkBg ? 'FFFFFF' : defaultPrimaryColor;

  // Calculate vertical positioning
  let totalElements = h1s.length + h2s.length + ps.length;
  let elementHeight = 0.8;
  let startY = isCentered ? Math.max(0.5, (5.625 - totalElements * elementHeight) / 2) : 0.5;
  let yPos = startY;

  // Add H1 (title)
  for (const el of h1s) {
    const color = parseColor(el.styles['color']) || defaultTitleColor;
    const align = isCentered ? 'center' : getAlignment(el.styles);

    slide.addText(el.text, {
      x: 0.5, y: yPos, w: 9, h: 1,
      fontSize: 44,
      fontFace: fontFamily,
      bold: true,
      color: color,
      align: align,
      valign: 'middle'
    });
    yPos += 1.2;
  }

  // Add H2 (subtitle)
  for (const el of h2s) {
    const color = parseColor(el.styles['color']) || defaultTitleColor;
    const align = isCentered ? 'center' : getAlignment(el.styles);

    slide.addText(el.text, {
      x: 0.5, y: yPos, w: 9, h: 0.8,
      fontSize: 32,
      fontFace: fontFamily,
      bold: true,
      color: color,
      align: align,
      valign: 'middle'
    });
    yPos += 1.0;
  }

  // Add paragraphs
  for (const el of ps) {
    const color = parseColor(el.styles['color']) || defaultTextColor;
    const align = isCentered ? 'center' : getAlignment(el.styles);

    slide.addText(el.text, {
      x: 0.5, y: yPos, w: 9, h: 0.6,
      fontSize: 20,
      fontFace: fontFamily,
      color: color,
      align: align,
      valign: 'middle'
    });
    yPos += 0.7;
  }

  // Add bullet lists
  for (const ulMatch of html.matchAll(/<ul[^>]*>([\s\S]*?)<\/ul>/gi)) {
    const liMatches = ulMatch[1].matchAll(/<li[^>]*>([\s\S]*?)<\/li>/gi);
    const items = [];
    for (const li of liMatches) {
      items.push({ text: stripHtml(li[1]), options: { bullet: true } });
    }

    if (items.length > 0) {
      slide.addText(items, {
        x: 0.5, y: yPos, w: 9, h: items.length * 0.45,
        fontSize: 18,
        fontFace: fontFamily,
        color: defaultTextColor,
        valign: 'top'
      });
      yPos += items.length * 0.45 + 0.3;
    }
  }
}

// Save
try {
  await pptx.writeFile({ fileName: outputPath });
  console.log(`Created: ${outputPath}`);
} catch (error) {
  console.error(`Error: ${error.message}`);
  process.exit(1);
}
