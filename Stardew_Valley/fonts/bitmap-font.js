/**
 * 星露谷位图字体渲染器 (AngelCode BMFont format)
 * 解析 .fnt + .png 并在 Canvas 上渲染文字
 */
(function () {
    'use strict';

    // ======== BMFont 解析器 ========
    class BMFont {
        constructor() {
            this.chars = new Map();
            this.kernings = new Map();
            this.lineHeight = 0;
            this.base = 0;
            this.scaleW = 0;
            this.scaleH = 0;
            this.image = null;
            this.ready = false;
            this.pending = [];
        }

        load(fntPath, pngPath) {
            return Promise.all([
                this._loadFnt(fntPath),
                this._loadImage(pngPath)
            ]).then(() => {
                this.ready = true;
                this.pending.forEach(fn => fn());
                this.pending = [];
            });
        }

        _loadFnt(url) {
            return fetch(url)
                .then(res => res.text())
                .then(xmlStr => {
                    const dom = new DOMParser().parseFromString(xmlStr, 'text/xml');
                    const font = dom.querySelector('font');
                    const common = font.querySelector('common');
                    this.lineHeight = parseInt(common.getAttribute('lineHeight'));
                    this.base = parseInt(common.getAttribute('base'));
                    this.scaleW = parseInt(common.getAttribute('scaleW'));
                    this.scaleH = parseInt(common.getAttribute('scaleH'));

                    font.querySelectorAll('char').forEach(el => {
                        const id = parseInt(el.getAttribute('id'));
                        this.chars.set(id, {
                            x: parseInt(el.getAttribute('x')),
                            y: parseInt(el.getAttribute('y')),
                            w: parseInt(el.getAttribute('width')),
                            h: parseInt(el.getAttribute('height')),
                            ox: parseInt(el.getAttribute('xoffset')),
                            oy: parseInt(el.getAttribute('yoffset')),
                            xa: parseInt(el.getAttribute('xadvance'))
                        });
                    });

                    // 解析 kernings（可选）
                    const kernEls = font.querySelector('kernings');
                    if (kernEls) {
                        kernEls.querySelectorAll('kerning').forEach(el => {
                            const first = parseInt(el.getAttribute('first'));
                            const second = parseInt(el.getAttribute('second'));
                            const amount = parseInt(el.getAttribute('amount'));
                            const key = first * 100000 + second;
                            this.kernings.set(key, amount);
                        });
                    }
                });
        }

        _loadImage(url) {
            return new Promise((resolve, reject) => {
                const img = new Image();
                img.crossOrigin = 'anonymous';
                img.onload = () => { this.image = img; resolve(); };
                img.onerror = reject;
                img.src = url;
            });
        }

        onReady(fn) {
            if (this.ready) { fn(); } else { this.pending.push(fn); }
        }

        getGlyph(code) {
            return this.chars.get(code) || this.chars.get(32);
        }

        getKerning(first, second) {
            return this.kernings.get(first * 100000 + second) || 0;
        }

        measureText(text, scale) {
            let w = 0;
            for (let i = 0; i < text.length; i++) {
                const g = this.getGlyph(text.charCodeAt(i));
                if (g) {
                    if (i > 0) {
                        w += this.getKerning(text.charCodeAt(i - 1), text.charCodeAt(i)) * scale;
                    }
                    w += g.xa * scale;
                }
            }
            return w;
        }

        /**
         * 渲染文字到 Canvas 并返回
         * @param {string} text
         * @param {object} opts
         * @param {number}  opts.fontSize    - 字号 (px)
         * @param {string}  opts.color       - 文字颜色
         * @param {boolean} opts.shadow      - 是否加阴影
         * @param {number}  opts.maxWidth    - 最大宽度(超出换行)
         * @returns {HTMLCanvasElement}
         */
        renderText(text, opts = {}) {
            const fontSize = opts.fontSize || 42;
            const scale = fontSize / this.base;
            const color = opts.color || '#ffffff';
            const shadow = opts.shadow !== false;
            const maxWidth = opts.maxWidth || Infinity;

            // 分词换行
            const lines = [];
            const words = String(text).split('');
            let curLine = '';
            let curW = 0;
            for (let i = 0; i < words.length; i++) {
                const ch = words[i];
                if (ch === '\n') {
                    lines.push(curLine);
                    curLine = '';
                    curW = 0;
                    continue;
                }
                const code = ch.charCodeAt(0);
                const g = this.getGlyph(code);
                const cw = g ? g.xa * scale : 0;
                if (curW + cw > maxWidth && curLine.length > 0) {
                    lines.push(curLine);
                    curLine = ch;
                    curW = cw;
                } else {
                    curLine += ch;
                    curW += cw;
                }
            }
            if (curLine) lines.push(curLine);

            const lh = this.lineHeight * scale;
            let maxLineW = 0;
            lines.forEach(line => {
                const mw = this.measureText(line, scale);
                if (mw > maxLineW) maxLineW = mw;
            });
            const totalH = lines.length * lh;

            const pad = 4;
            const canvas = document.createElement('canvas');
            canvas.width = Math.ceil(maxLineW) + pad * 2;
            canvas.height = Math.ceil(totalH) + pad * 2;
            const ctx = canvas.getContext('2d');

            for (let li = 0; li < lines.length; li++) {
                const line = lines[li];
                let x = pad;
                const y = pad + li * lh;

                for (let i = 0; i < line.length; i++) {
                    const code = line.charCodeAt(i);
                    const g = this.getGlyph(code);
                    if (!g) continue;

                    if (i > 0) {
                        x += this.getKerning(line.charCodeAt(i - 1), code) * scale;
                    }

                    const sx = g.x;
                    const sy = g.y;
                    const sw = g.w;
                    const sh = g.h;
                    const dx = x + g.ox * scale;
                    const dy = y + g.oy * scale;
                    const dw = sw * scale;
                    const dh = sh * scale;

                    // 绘制该字符
                    if (this.image) {
                        ctx.drawImage(this.image, sx, sy, sw, sh, dx, dy, dw, dh);
                    }

                    x += g.xa * scale;
                }
            }

            // 用颜色着色 (将原图白色区域替换为目标颜色)
            if (color !== '#ffffff') {
                const imgData = ctx.getImageData(0, 0, canvas.width, canvas.height);
                const data = imgData.data;
                // 解析颜色
                const tmp = document.createElement('div');
                tmp.style.color = color;
                document.body.appendChild(tmp);
                const cs = getComputedStyle(tmp).color;
                document.body.removeChild(tmp);
                const match = cs.match(/\d+/g);
                const r = parseInt(match[0]), g2 = parseInt(match[1]), b = parseInt(match[2]);

                for (let i = 0; i < data.length; i += 4) {
                    if (data[i] > 10 || data[i + 1] > 10 || data[i + 2] > 10) {
                        // 保留原 alpha，替换颜色
                        const alpha = data[i + 3];
                        data[i] = r;
                        data[i + 1] = g2;
                        data[i + 2] = b;
                        data[i + 3] = alpha;
                    }
                }
                ctx.putImageData(imgData, 0, 0);
            }

            // 添加阴影（绘制到最终 canvas 上）
            if (shadow) {
                const finalCanvas = document.createElement('canvas');
                finalCanvas.width = canvas.width + 4;
                finalCanvas.height = canvas.height + 4;
                const fctx = finalCanvas.getContext('2d');
                // 阴影
                fctx.shadowColor = 'rgba(0,0,0,0.45)';
                fctx.shadowBlur = 3;
                fctx.shadowOffsetX = 1;
                fctx.shadowOffsetY = 2;
                fctx.drawImage(canvas, 2, 2);
                // 清除阴影
                fctx.shadowColor = 'transparent';
                fctx.drawImage(canvas, 2, 2);
                return finalCanvas;
            }

            return canvas;
        }
    }

    // ======== 全局实例 ========
    const stardewFont = new BMFont();

    // ======== 工具函数：将 Canvas 文字动态插入页面 ========
    const replacedElements = new WeakMap();

    /**
     * 将元素中的文字替换为 Canvas 渲染的位图字体
     * @param {HTMLElement} el - 目标元素
     * @param {object} opts - 渲染选项
     */
    function applyFontToElement(el, opts = {}) {
        if (!stardewFont.ready) {
            stardewFont.onReady(() => applyFontToElement(el, opts));
            return;
        }

        const text = el.textContent;
        if (!text.trim()) return;

        // 计算字号：从 CSS 中读取
        const cs = getComputedStyle(el);
        let fontSize = opts.fontSize || parseFloat(cs.fontSize) || 16;
        // 根据父容器缩放比例调整
        const color = opts.color || cs.color || '#3d2f1f';
        const maxWidth = opts.maxWidth || el.clientWidth || 600;

        const canvas = stardewFont.renderText(text, {
            fontSize: fontSize * 1.0,  // 位图字体与 CSS 字号保持一致，防止换行
            color: color,
            shadow: true,
            maxWidth: maxWidth
        });

        // 保存原始文本和 canvas
        replacedElements.set(el, { original: text, canvas: canvas });

        // 替换元素内容
        el.innerHTML = '';
        canvas.style.display = 'inline';
        canvas.style.verticalAlign = 'middle';
        el.appendChild(canvas);

        // 隐藏原始文字闪烁（使用 visibility 过渡）
        el.style.overflow = 'visible';
    }

    /**
     * 将页面中所有文本元素替换为位图字体渲染
     * 小字号 (fontSize < 14px) 自动取消阴影
     */
    function applyToAll(opts = {}) {
        // 排除的标签（输入框、脚本、图片等）
        const SKIP_TAGS = new Set(['INPUT','TEXTAREA','SELECT','OPTION','SCRIPT','STYLE','CANVAS','IMG','BR','HR','SVG','PRE','CODE','NOSCRIPT']);
        // 覆盖所有网页的文本元素选择器
        const SELECTORS = [
            // 标题
            'h1', 'h2', 'h3', 'h4', 'h5', 'h6',
            // 导航 & 品牌
            '.nav-brand', '.nav-link', '.login-link', '.user-avatar', '.logout-btn',
            // 商店页
            '.header h1', '.header p', '.stats-bar span',
            '.item-name', '.item-price', '.item-category', '.item-source',
            '#loadingMsg', '#errorMsg',
            '.cart-sidebar-header h3', '.cart-sidebar-item-name',
            '.sidebar-item-price', '.sidebar-item-subtotal',
            '.total-items', '.total-price',
            '.checkout-btn', '.detail-add-btn',
            '.cart-sidebar-empty',
            // 新闻页
            '.news-column-header h2', '.news-column-motto',
            '.news-card-title', '.news-card-summary', '.news-card-meta', '.news-card-badge',
            '.news-sidebar-title', '.news-sidebar-item',
            '.placeholder-card',
            // 配送页
            '.delivery-title h1', '.delivery-title p',
            '.delivery-intro p', '.delivery-card h3', '.delivery-card p',
            '.delivery-status p', '.delivery-step span', '.delivery-step p',
            '.faq-item h4', '.faq-item p',
            // 登录页
            '.login-header h1', '.login-header p', '.login-header .avatar',
            '.login-container p', '.form-group label',
            '.submit-btn', '.back-link a',
            // 表单
            'label',
            // 表格
            'th', 'td',
            // 页脚
            'footer',
            // 自定义钩子
            '[data-stardew-font]', '.stardew-font',
        ].join(',');

        document.querySelectorAll(SELECTORS).forEach(el => {
            // 跳过已处理的
            if (replacedElements.has(el)) return;
            if (SKIP_TAGS.has(el.tagName)) return;
            // 跳过已包含 canvas 的（防止重复替换）
            if (el.querySelector('canvas')) return;
            // 跳过有复杂子元素的（需要保留内部结构）
            const text = el.textContent.trim();
            if (!text || text.length < 1) return;
            // 如果元素有多个子元素且不仅仅是纯文本，跳过整体替换
            //（它的子元素会被单独匹配）
            const childEls = Array.from(el.children).filter(c => c.tagName !== 'CANVAS');
            if (childEls.length > 0) return;

            // 根据字号决定是否加阴影（小字号不加）
            const fontSize = parseFloat(getComputedStyle(el).fontSize) || 14;
            const useShadow = (opts.shadow !== undefined) ? opts.shadow : (fontSize >= 14);
            applyFontToElement(el, Object.assign({}, opts, { shadow: useShadow }));
        });
    }

    // ======== 暴露全局 API ========
    window.StardewFont = {
        font: stardewFont,
        apply: applyFontToElement,
        applyToAll: applyToAll,
        load: function (fntPath, pngPath) {
            return stardewFont.load(fntPath, pngPath).then(() => {
                // 加载完成后自动应用
                applyToAll();
            });
        }
    };
})();