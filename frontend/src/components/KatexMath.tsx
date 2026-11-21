import React, { useMemo } from 'react';
import katex from 'katex';

interface KatexMathProps {
  math: string;
  block?: boolean;
  className?: string;
}

export const KatexMath: React.FC<KatexMathProps> = ({ math, block = true, className = '' }) => {
  const html = useMemo(() => {
    if (!math) return '';
    try {
      let cleanMath = math.trim();
      // Remove enclosing $$, $, \[, \] if present
      if (cleanMath.startsWith('$$') && cleanMath.endsWith('$$') && cleanMath.length >= 4) {
        cleanMath = cleanMath.slice(2, -2).trim();
      } else if (cleanMath.startsWith('$') && cleanMath.endsWith('$') && cleanMath.length >= 2) {
        cleanMath = cleanMath.slice(1, -1).trim();
      } else if (cleanMath.startsWith('\\[') && cleanMath.endsWith('\\]') && cleanMath.length >= 4) {
        cleanMath = cleanMath.slice(2, -2).trim();
      }

      return katex.renderToString(cleanMath, {
        displayMode: block,
        throwOnError: false,
      });
    } catch (err) {
      console.warn('KaTeX rendering error:', err);
      return `<span class="text-amber-400 font-mono text-xs">${escapeHtml(math)}</span>`;
    }
  }, [math, block]);

  return (
    <div
      className={`katex-math-wrapper ${block ? 'my-1 overflow-x-auto text-center' : 'inline-block'} ${className}`}
      dangerouslySetInnerHTML={{ __html: html }}
    />
  );
};

function escapeHtml(str: string): string {
  return str
    .replace(/&/g, '&amp;')
    .replace(/</g, '&lt;')
    .replace(/>/g, '&gt;')
    .replace(/"/g, '&quot;')
    .replace(/'/g, '&#039;');
}
