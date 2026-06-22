const fs = require('fs');
const path = require('path');
const { execSync } = require('child_process');

// 极简桌面扫描器 —— 100% 本地，无网络依赖
console.log('\n🔍 正在扫描桌面文档...');

const desktop = process.env.USERPROFILE + '\\Desktop';
const ollamaPath = path.join(__dirname, 'ollama.js');

function scanDir(dir) {
  try {
    const entries = fs.readdirSync(dir, { withFileTypes: true });
    for (const entry of entries) {
      const fullPath = path.join(dir, entry.name);

      if (entry.isDirectory()) continue; // 只处理文件，不递归

      const ext = path.extname(entry.name).toLowerCase();
      const validExts = ['.md', '.txt', '.py', '.js', '.ts', '.json', '.yaml', '.yml', '.html', '.css', '.java', '.cpp', '.go', '.rs', '.sh', '.bat', '.ps1'];
      if (!validExts.includes(ext)) continue;

      try {
        let content = fs.readFileSync(fullPath, 'utf8').slice(0, 4096);
        if (content.trim().length < 10) continue;

        // 生成嵌入向量
        const embResult = JSON.parse(execSync(`node ${ollamaPath} embed "${content.substring(0, 256)}"`).toString());
        
        // 存入知识库
        const docId = `desktop:${Date.now()}:${Math.random().toString(36).substr(2, 9)}`;
        const storePath = path.join(__dirname, '..', '..', '..', 'state', 'gbrain', 'auto-scan');
        if (!fs.existsSync(storePath)) {
          fs.mkdirSync(storePath, { recursive: true });
        }
        
        // 简单 JSON 存储（绕过 storage.js）
        const storeFile = path.join(storePath, 'store.json');
        let store = [];
        try {
          store = JSON.parse(fs.readFileSync(storeFile, 'utf8'));
        } catch (e) {}
        
        store.push({
          id: docId,
          title: entry.name,
          content,
          source: fullPath,
          timestamp: new Date().toISOString(),
          embedding: embResult.embedding
        });
        
        fs.writeFileSync(storeFile, JSON.stringify(store, null, 2));
        
        console.log(`[✓] indexed ${fullPath} (${embResult.embedding.length}d)`);
      } catch (e) {
        // console.error(`[✗] skip ${fullPath}: ${e.message}`);
      }
    }
  } catch (e) {
    console.error(`[✗] access denied ${desktop}: ${e.message}`);
  }
}

scanDir(desktop);
console.log('\n✅ 桌面扫描完成！');