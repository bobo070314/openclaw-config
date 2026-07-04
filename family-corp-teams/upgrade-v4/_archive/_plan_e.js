const http = require('http');
const data = JSON.stringify({
    model: 'openclaw',
    messages: [{ role: 'user', content: '/goal start IGP v4终极升级 - 42Team集体研究突破，引擎8.5/10' }]
});
const req = http.request({
    hostname: '127.0.0.1', port: 18900,
    path: '/v1/chat/completions', method: 'POST',
    headers: { 'Content-Type': 'application/json', 'Authorization': 'Bearer ***' }
}, (res) => {
    let body = ''; res.on('data', d => body += d);
    res.on('end', () => console.log(res.statusCode, body.slice(0,200)));
});
req.on('error', e => console.log('ERR:', e.message));
req.write(data); req.end();
