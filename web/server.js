const http = require('http');
const fs = require('fs');
const path = require('path');
const url = require('url');

const PORT = 8001;

// 静态文件MIME类型
const mimeTypes = {
    '.html': 'text/html',
    '.js': 'text/javascript',
    '.css': 'text/css',
    '.json': 'application/json',
    '.png': 'image/png',
    '.jpg': 'image/jpg',
    '.gif': 'image/gif',
    '.ico': 'image/x-icon',
    '.svg': 'image/svg+xml'
};

const server = http.createServer((req, res) => {
    const parsedUrl = url.parse(req.url, true);
    const pathname = parsedUrl.pathname;

    // CORS 头
    res.setHeader('Access-Control-Allow-Origin', '*');
    res.setHeader('Access-Control-Allow-Methods', 'GET, POST, PUT, DELETE, OPTIONS');
    res.setHeader('Access-Control-Allow-Headers', 'Content-Type, Authorization');

    // 处理 OPTIONS 请求
    if (req.method === 'OPTIONS') {
        res.writeHead(200);
        res.end();
        return;
    }

    // API: 写入文件
    if (pathname === '/api/write-file' && req.method === 'POST') {
        let body = '';
        req.on('data', chunk => {
            body += chunk.toString();
        });

        req.on('end', () => {
            try {
                const { filePath, content } = JSON.parse(body);

                if (!filePath || content === undefined) {
                    res.writeHead(400, { 'Content-Type': 'application/json' });
                    res.end(JSON.stringify({ error: '文件路径和内容不能为空' }));
                    return;
                }

                // 确保目录存在
                const dir = path.dirname(filePath);
                fs.mkdirSync(dir, { recursive: true });

                // 写入文件
                fs.writeFileSync(filePath, content, 'utf8');

                console.log(`✅ 文件写入成功: ${filePath}`);

                res.writeHead(200, { 'Content-Type': 'application/json' });
                res.end(JSON.stringify({
                    success: true,
                    message: '文件写入成功',
                    path: filePath
                }));

            } catch (error) {
                console.error('写入文件失败:', error);
                res.writeHead(500, { 'Content-Type': 'application/json' });
                res.end(JSON.stringify({ error: '写入文件失败: ' + error.message }));
            }
        });
        return;
    }

    // API: 读取文件
    if (pathname === '/api/read-file' && req.method === 'POST') {
        let body = '';
        req.on('data', chunk => {
            body += chunk.toString();
        });

        req.on('end', () => {
            try {
                const { filePath } = JSON.parse(body);

                if (!filePath) {
                    res.writeHead(400, { 'Content-Type': 'application/json' });
                    res.end(JSON.stringify({ error: '文件路径不能为空' }));
                    return;
                }

                // 检查文件是否存在
                if (!fs.existsSync(filePath)) {
                    res.writeHead(404, { 'Content-Type': 'application/json' });
                    res.end(JSON.stringify({ error: '文件不存在' }));
                    return;
                }

                // 读取文件
                const content = fs.readFileSync(filePath, 'utf8');

                console.log(`✅ 文件读取成功: ${filePath}`);

                res.writeHead(200, { 'Content-Type': 'application/json' });
                res.end(JSON.stringify({
                    success: true,
                    content: content,
                    path: filePath
                }));

            } catch (error) {
                console.error('读取文件失败:', error);
                res.writeHead(500, { 'Content-Type': 'application/json' });
                res.end(JSON.stringify({ error: '读取文件失败: ' + error.message }));
            }
        });
        return;
    }

    // API: 创建项目目录
    if (pathname === '/api/create-directory' && req.method === 'POST') {
        let body = '';
        req.on('data', chunk => {
            body += chunk.toString();
        });

        req.on('end', () => {
            try {
                const { projectName } = JSON.parse(body);

                if (!projectName) {
                    res.writeHead(400, { 'Content-Type': 'application/json' });
                    res.end(JSON.stringify({ error: '项目名称不能为空' }));
                    return;
                }

                // 创建项目目录
                const projectPath = path.join(__dirname, 'project', projectName);
                const sourcePath = path.join(projectPath, 'source');
                const paperPath = path.join(projectPath, 'paper');

                // 创建目录
                fs.mkdirSync(projectPath, { recursive: true });
                fs.mkdirSync(sourcePath, { recursive: true });
                fs.mkdirSync(paperPath, { recursive: true });

                console.log(`✅ 项目目录创建成功: ${projectPath}`);

                res.writeHead(200, { 'Content-Type': 'application/json' });
                res.end(JSON.stringify({
                    success: true,
                    message: '项目目录创建成功',
                    path: projectPath
                }));

            } catch (error) {
                console.error('创建目录失败:', error);
                res.writeHead(500, { 'Content-Type': 'application/json' });
                res.end(JSON.stringify({ error: '创建目录失败: ' + error.message }));
            }
        });
        return;
    }

    // 静态文件服务
    let filePath = '.' + pathname;
    if (filePath === './') {
        filePath = './index.html';
    }

    const extname = String(path.extname(filePath)).toLowerCase();
    const contentType = mimeTypes[extname] || 'application/octet-stream';

    fs.readFile(filePath, (error, content) => {
        if (error) {
            if (error.code === 'ENOENT') {
                res.writeHead(404, { 'Content-Type': 'text/html' });
                res.end('404 - File Not Found', 'utf-8');
            } else {
                res.writeHead(500);
                res.end('Server Error: ' + error.code + ' ..\n');
            }
        } else {
            res.writeHead(200, { 'Content-Type': contentType });
            res.end(content, 'utf-8');
        }
    });
});

server.listen(PORT, () => {
    console.log(`🚀 服务器运行在 http://localhost:${PORT}`);
    console.log(`📁 项目目录: ${path.join(__dirname, 'project')}`);
});