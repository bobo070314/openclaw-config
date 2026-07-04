
const WebSocket = require('ws');
const http = require('http');

async function run() {
    // 尝试HTTP API发/goal start
    const data = JSON.stringify({
        model: 'openclaw',
        messages: [{ role: 'user', content: '/goal start ' + JSON.stringify('IGP v4终极升级 - 42Team集体研究突破，引擎8.5/10') }]
    });
    const options = {
        hostname: '127.0.0.1', port: 18900, path: '/v1/chat/completions',
        method: 'POST',
        headers: { 'Content-Type': 'application/json' }
    };
    return new Promise((resolve) => {
        const req = http.request(options, (res) => {
            let body = '';
            res.on('data', d => body += d);
            res.on('end', () => resolve({ status: res.statusCode, body: body.slice(0, 300) }));
        });
        req.on('error', (e) => resolve({ error: e.message }));
        req.write(data);
        req.end();
    });
}
run().then(console.log).catch(console.error);
