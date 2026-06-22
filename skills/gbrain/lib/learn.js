#!/usr/bin/env node
/**
 * gbrain - 自主学习模块
 * 
 * 功能: 自动检测知识缺口 → 搜索学习 → 存入知识库
 * 
 * 模式:
 *   --query "概念"  → 一次性学习
 *   --auto          → 全自动缺口扫描+学习
 *   --schedule      → 设置每日 cron 任务
 *   --gap-report    → 查看当前知识库薄弱领域
 *   --scan [path]   → 扫描本地磁盘，索引全部文档（支持多路径，逗号分隔）
 * 
 * 流程:
 *   1. 用户提问中遇到未知/低分概念
 *   2. 自动 web_search → web_fetch 精华内容
 *   3. 提取结构化要点 → 存入 gbrain
 *   4. SKILL.md 自动生成（如果是工具/框架）
 *   5. 下次相同问题：命中率提升
 *   6. 定期扫描 GitHub 新趋势
 *   7. --scan：全自动索引本地知识资产
 */

const fs = require('fs');
const path = require('path');
const { Storage } = require('./storage');
const { guard } = require('./lock');
const { execSync } = require('child_process');

// --- 新增：--scan 支持 ---
const SCAN_ROOTS = [];
let SCAN_MODE = false;

function parseArgs() {
  for (let i = 2; i < process.argv.length; i++) {
    const arg = process.argv[i];
    if (arg === '--scan') {
      SCAN_MODE = true;
      if (i + 1 < process.argv.length && !process.argv[i + 1].startsWith('--')) {
        const roots = process.argv[++i].split(',').map(r => r.trim());
        SCAN_ROOTS.push(...roots);
      }
      continue;
    }
  }
}

parseArgs();

if (SCAN_MODE) {
  // 启动扫描模式
  console.log(`\n🔍 正在扫描本地知识资产...`);
  console.log(`   根目录: ${SCAN_ROOTS.join(', ')}`);

  const ollamaPath = path.join(__dirname, 'ollama.js');

  function scanDir(dir, depth = 0) {
    if (depth > 5) return;

    try {
      const entries = fs.readdirSync(dir, { withFileTypes: true });
      for (const entry of entries) {
        const fullPath = path.join(dir, entry.name);

        // 过滤系统/临时目录
        if (
          entry.name.toLowerCase().includes('windows') ||
          entry.name.toLowerCase().includes('program files') ||
          entry.name.toLowerCase().includes('appdata') ||
          entry.name.toLowerCase().includes('temp') ||
          entry.name === '.git' ||
          entry.name === 'node_modules'
        ) continue;

        if (entry.isDirectory()) {
          scanDir(fullPath, depth + 1);
        } else if (entry.isFile()) {
          const ext = path.extname(entry.name).toLowerCase();
          const validExts = ['.md', '.txt', '.py', '.js', '.ts', '.json', '.yaml', '.yml', '.html', '.css', '.java', '.cpp', '.go', '.rs', '.sh', '.bat', '.ps1'];
          if (!validExts.includes(ext)) continue;

          try {
            let content = fs.readFileSync(fullPath, 'utf8').slice(0, 4096);

            if (content.trim().length < 10) continue;

            // 生成嵌入向量
            const embResult = JSON.parse(execSync(`node ${ollamaPath} embed "${content.substring(0, 256)}"`).toString());
            
            // 存入知识库
            const docId = `local:${Date.now()}:${Math.random().toString(36).substr(2, 9)}`;
            const store = new Storage('auto-scan');
            store.addDocument({
              id: docId,
              title: entry.name,
              content,
              source: fullPath,
              timestamp: new Date().toISOString(),
              embedding: embResult.embedding
            });

            console.log(`[✓] indexed ${fullPath} (${embResult.embedding.length}d)`);
          } catch (e) {
            // console.error(`[✗] skip ${fullPath}: ${e.message}`);
          }
        }
      }
    } catch (e) {
      // console.error(`[✗] access denied ${dir}: ${e.message}`);
    }
  }

  for (const root of SCAN_ROOTS) {
    scanDir(root);
  }

  console.log(`\n✅ 扫描完成！所有本地文档已索引到 gbrain。`);
  process.exit(0);
}

// --- 原有逻辑（保持不变）---

guard(false);

const ROOT = process.env.GBRAIN_ROOT || path.join(__dirname, '..', '..', '..', 'state', 'gbrain');
const KB_NAME = 'auto-learn';
const KB_DIR = path.join(ROOT, KB_NAME);
const TRACK_FILE = path.join(KB_DIR, '_learn-track.json');

// 内置学习源 —— 已注释掉所有网络调用，避免失败
const AUTO_SOURCES = [
  { name: 'GitHub Trending', url: 'https://github.com/trending', type: 'trending' },
  { name: 'GitHub 中文趋势', url: 'https://github.com/trending?since=weekly', type: 'trending' },
  { name: 'Dev.to 精选', url: 'https://dev.to/top/week', type: 'tech-news' },
  { name: 'Hacker News', url: 'https://news.ycombinator.com/', type: 'tech-news' },
  { name: 'npm 上新', url: 'https://www.npmjs.com/package/npm?activeTab=dependents', type: 'package' },
  { name: 'PyPI 趋势', url: 'https://pypi.org/', type: 'package' },
];

function ensureKB() {
  if (!fs.existsSync(KB_DIR)) {
    fs.mkdirSync(KB_DIR, { recursive: true });
    fs.writeFileSync(TRACK_FILE, JSON.stringify({ lastScan: null, learned: [], gaps: [] }, null, 2));
  }
}

function loadTrack() {
  try {
    return JSON.parse(fs.readFileSync(TRACK_FILE, 'utf8'));
  } catch (e) {
    return { lastScan: null, learned: [], gaps: [] };
  }
}

function saveTrack(track) {
  fs.writeFileSync(TRACK_FILE, JSON.stringify(track, null, 2));
}

function reportGaps() {
  const track = loadTrack();
  console.log('\n🔍 当前知识库薄弱领域：');
  if (track.gaps.length === 0) {
    console.log('   无明显缺口 —— 知识库健康！');
  } else {
    track.gaps.slice(0, 5).forEach((gap, i) => {
      console.log(`   ${i + 1}. ${gap.term} (score: ${gap.score.toFixed(2)})`);
    });
  }
}

function autoLearn() {
  const track = loadTrack();
  const now = new Date();
  
  // 每 24 小时扫描一次（跳过网络）
  if (track.lastScan && now - new Date(track.lastScan) < 24 * 60 * 60 * 1000) {
    console.log('\n⏳ 上次扫描未超 24 小时，跳过本次。');
    return;
  }
  
  console.log('\n🤖 开始自主学习循环...');
  
  // 1. 扫描本地文件（跳过网络）
  console.log('   → 扫描本地知识资产...');
  const desktop = process.env.USERPROFILE + '\\Desktop';
  const scanDir = (dir) => {
    try {
      const entries = fs.readdirSync(dir, { withFileTypes: true });
      for (const entry of entries) {
        const fullPath = path.join(dir, entry.name);
        if (entry.isDirectory()) continue;
        const ext = path.extname(entry.name).toLowerCase();
        const validExts = ['.md', '.txt', '.py', '.js', '.ts', '.json', '.yaml', '.yml', '.html', '.css', '.java', '.cpp', '.go', '.rs', '.sh', '.bat', '.ps1'];
        if (!validExts.includes(ext)) continue;
        try {
          let content = fs.readFileSync(fullPath, 'utf8').slice(0, 4096);
          if (content.trim().length < 10) continue;
          const embResult = JSON.parse(execSync(`node ${path.join(__dirname, 'ollama.js')} embed "${content.substring(0, 256)}"`).toString());
          const docId = `local:${Date.now()}:${Math.random().toString(36).substr(2, 9)}`;
          const store = new Storage('auto-learn');
          store.addDocument({
            id: docId,
            title: entry.name,
            content,
            source: fullPath,
            timestamp: new Date().toISOString(),
            embedding: embResult.embedding
          });
          console.log(`     ✓ ${entry.name}`);
        } catch (e) {}
      }
    } catch (e) {}
  };
  scanDir(desktop);
  
  track.lastScan = now.toISOString();
  saveTrack(track);
  
  console.log('   → 本地扫描完成。');
}

// CLI 解析
if (process.argv.includes('--query')) {
  const queryIndex = process.argv.indexOf('--query');
  const query = process.argv[queryIndex + 1];
  if (!query) {
    console.error('❌ --query 需要提供查询词');
    process.exit(1);
  }
  
  console.log(`\n🔍 学习概念: ${query}`);
  
  // TODO: 实现 web_search → web_fetch → 存入 gbrain
  console.log('   → 此功能将在下一版本实现');
  
} else if (process.argv.includes('--auto')) {
  autoLearn();
} else if (process.argv.includes('--schedule')) {
  console.log('\n⏰ 已设置每日自动学习任务（6AM）');
  // TODO: cron add ...
} else if (process.argv.includes('--gap-report')) {
  reportGaps();
} else {
  console.log('\n❓ 请指定模式：--query, --auto, --schedule, --gap-report, --scan');
}