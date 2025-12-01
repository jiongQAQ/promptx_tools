/**
 * CNKI Search - 知网论文搜索工具
 * 
 * 战略意义：
 * 1. 学术资源接入：为AI提供真实可用的中文学术资源检索能力
 * 2. 浏览器自动化：使用Puppeteer模拟真实用户行为，绕过反爬机制
 * 3. 生态扩展性：作为学术工具的基础，可扩展为完整的文献管理体系
 * 
 * 设计理念：
 * 使用Puppeteer（无头浏览器）而非简单HTTP请求，这是目前爬取知网最可靠的方案。
 * 通过真实浏览器环境执行JavaScript，获取动态渲染的内容。
 * 模拟人类操作习惯，包括合理的等待时间，降低被检测风险。
 * 优先使用系统已安装的Chrome浏览器，避免下载Chromium。
 * 
 * 技术要点：
 * - 需要本地安装Chrome浏览器
 * - 相比HTTP请求更慢但更可靠
 * - 自动查找系统Chrome路径
 */

module.exports = {
  getDependencies() {
    return {
      'puppeteer': '^21.0.0'
    };
  },

  getMetadata() {
    return {
      id: 'cnki-search',
      name: 'CNKI知网搜索',
      description: '使用Puppeteer真实搜索知网论文，获取标题、作者等基本信息',
      version: '3.1.0',
      author: '鲁班'
    };
  },

  getSchema() {
    return {
      parameters: {
        type: 'object',
        properties: {
          keyword: {
            type: 'string',
            description: '搜索关键词',
            minLength: 1,
            maxLength: 100
          },
          limit: {
            type: 'number',
            description: '返回结果数量',
            minimum: 1,
            maximum: 50,
            default: 10
          },
          headless: {
            type: 'boolean',
            description: '是否使用无头模式（true=后台运行，false=显示浏览器）',
            default: true
          }
        },
        required: ['keyword']
      }
    };
  },

  async execute(params) {
    const { api } = this;
    const { keyword, limit = 10, headless = true } = params;

    api.logger.info('开始启动Puppeteer', { keyword, limit });

    let browser = null;
    
    try {
      const puppeteer = await api.importx('puppeteer');

      // 检测系统Chrome路径
      const chromePaths = [
        '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome',  // macOS
        '/Applications/Chromium.app/Contents/MacOS/Chromium',            // macOS Chromium
        'C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe',     // Windows
        'C:\\Program Files (x86)\\Google\\Chrome\\Application\\chrome.exe',
        '/usr/bin/google-chrome',                                        // Linux
        '/usr/bin/chromium-browser',                                     // Linux
        '/snap/bin/chromium'                                             // Linux Snap
      ];

      let executablePath = null;
      const fs = await api.importx('fs');
      
      for (const path of chromePaths) {
        try {
          if (fs.existsSync(path)) {
            executablePath = path;
            api.logger.info('找到Chrome浏览器', { path });
            break;
          }
        } catch (e) {
          // 忽略
        }
      }

      // 启动浏览器配置
      const launchOptions = {
        headless: headless ? 'new' : false,
        args: [
          '--no-sandbox',
          '--disable-setuid-sandbox',
          '--disable-dev-shm-usage',
          '--disable-accelerated-2d-canvas',
          '--disable-gpu',
          '--window-size=1920,1080'
        ]
      };

      // 如果找到系统Chrome，使用它
      if (executablePath) {
        launchOptions.executablePath = executablePath;
      } else {
        api.logger.warn('未找到系统Chrome，将使用Puppeteer内置Chromium');
      }

      // 启动浏览器
      browser = await puppeteer.launch(launchOptions);

      api.logger.info('浏览器启动成功');

      const page = await browser.newPage();
      
      // 设置视口
      await page.setViewport({ width: 1920, height: 1080 });
      
      // 设置User-Agent
      await page.setUserAgent('Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36');

      // 构造搜索URL
      const searchUrl = `https://kns.cnki.net/kns8/defaultresult/index?crossids=YSTT4HG0,C816MT8M&kw=${encodeURIComponent(keyword)}&korder=SU`;
      
      api.logger.info('访问知网搜索页面', { url: searchUrl });

      // 访问搜索页面
      await page.goto(searchUrl, {
        waitUntil: 'networkidle2',
        timeout: 30000
      });

      api.logger.info('页面加载完成，等待内容渲染');

      // 等待搜索结果加载
      await page.waitForTimeout(3000);

      // 提取搜索结果
      const results = await page.evaluate((maxResults) => {
        const items = [];
        
        // 尝试多种可能的选择器
        const selectors = [
          'table.result-table-list tbody tr',
          '.result-table-list tr',
          'tr[id]',
          '.list-item'
        ];

        let elements = [];
        for (const selector of selectors) {
          elements = document.querySelectorAll(selector);
          if (elements.length > 0) break;
        }

        for (let i = 0; i < Math.min(elements.length, maxResults); i++) {
          const row = elements[i];
          
          // 查找标题链接
          const titleLink = row.querySelector('a.fz14, a[href*="kcms"], a[href*="Detail"]');
          if (!titleLink) continue;

          const title = titleLink.textContent.trim();
          if (!title || title.length < 5) continue;

          // 提取其他信息
          const allCells = row.querySelectorAll('td');
          let author = '';
          let source = '';
          let date = '';

          // 根据表格结构提取
          if (allCells.length >= 5) {
            author = allCells[2]?.textContent.trim() || '';
            source = allCells[3]?.textContent.trim() || '';
            date = allCells[4]?.textContent.trim() || '';
          }

          // 提取链接
          let link = titleLink.href || '';
          if (link && !link.startsWith('http')) {
            link = 'https://kns.cnki.net' + link;
          }

          items.push({
            title,
            author: author || '未知',
            source: source || '未知',
            date: date || '未知',
            link
          });
        }

        return items;
      }, limit);

      await browser.close();
      browser = null;

      api.logger.info('提取完成', { count: results.length });

      if (results.length === 0) {
        return {
          success: false,
          message: '未找到相关论文',
          suggestion: '1) 尝试更换关键词 2) 检查知网是否正常访问 3) 查看日志了解详情',
          keyword,
          count: 0
        };
      }

      return {
        success: true,
        message: `成功找到 ${results.length} 篇论文`,
        data: results,
        keyword,
        count: results.length,
        note: '使用Puppeteer真实浏览器爬取'
      };

    } catch (error) {
      // 确保浏览器关闭
      if (browser) {
        try {
          await browser.close();
        } catch (e) {
          api.logger.error('关闭浏览器失败', { error: e.message });
        }
      }

      api.logger.error('搜索失败', { 
        error: error.message,
        stack: error.stack
      });

      let suggestion = '搜索出错，请稍后重试';
      
      if (error.message.includes('Could not find Chrome') || error.message.includes('Could not find browser')) {
        suggestion = '未找到Chrome浏览器。请确保已安装Chrome，或者设置PUPPETEER_SKIP_CHROMIUM_DOWNLOAD=false让Puppeteer下载Chromium';
      } else if (error.message.includes('timeout')) {
        suggestion = '页面加载超时，知网响应较慢，请重试';
      } else if (error.message.includes('Navigation failed')) {
        suggestion = '无法访问知网，请检查网络连接';
      }

      return {
        success: false,
        error: error.message,
        suggestion,
        keyword
      };
    }
  },

  getBusinessErrors() {
    return [
      {
        code: 'CHROME_NOT_FOUND',
        description: '找不到Chrome浏览器',
        match: /Could not find Chrome|Could not find browser/i,
        solution: '请安装Chrome浏览器，或配置executablePath指向Chrome路径',
        retryable: false
      },
      {
        code: 'NAVIGATION_TIMEOUT',
        description: '页面加载超时',
        match: /timeout|Navigation timeout/i,
        solution: '知网响应较慢，请重试或增加超时时间',
        retryable: true
      },
      {
        code: 'NETWORK_ERROR',
        description: '网络连接失败',
        match: /Navigation failed|net::ERR/i,
        solution: '检查网络连接，确保能访问知网',
        retryable: true
      }
    ];
  }
};