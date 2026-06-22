#!/usr/bin/env node
/**
 * gbrain Git 集成插件
 * 
 * 将 Git 仓库的代码变更、PR、提交记录索引到 gbrain 知识库。
 * 
 * 功能:
 * - 索引整个 git 仓库结构到知识库
 * - 监控并索引新提交的 diff
 * - 索引 README 和文档
 * - 支持 GitHub/GitLab PR 探测
 * - 自动检测 git worktree
 */

const { execSync } = require('child_process');
const fs = require('fs');
const path = require('path');

const GBRAIN_LIB = path.resolve(__dirname, '..', 'lib');

function getStorage() {
  return require(path.join(GBRAIN_LIB, 'storage'));
}

function guard() {
  try {
    require(path.join(GBRAIN_LIB, 'lock')).guard(false);
  } catch (e) {
    console.error('🔒 Guard failed:', e.message);
    process.exit(1);
  }
}

// ========================================
// Git 工具函数
// ========================================

function isGitRepo(dir) {
  try {
    execSync(`git rev-parse --is-inside-work-tree`, { cwd: dir, encoding: 'utf-8', stdio: 'pipe' });
    return true;
  } catch { return false; }
}

function getRoot(dir) {
  return execSync(`git rev-parse --show-toplevel`, { cwd: dir, encoding: 'utf-8' }).trim();
}

function getRemoteUrl(dir) {
  try {
    return execSync(`git remote get-url origin`, { cwd: dir, encoding: 'utf-8' }).trim();
  } catch { return null; }
}

function getCurrentBranch(dir) {
  return execSync(`git rev-parse --abbrev-ref HEAD`, { cwd: dir, encoding: 'utf-8' }).trim();
}

function getRecentCommits(dir, count = 20) {
  const output = execSync(`git log --oneline -${count}`, { cwd: dir, encoding: 'utf-8' }).trim();
  return output.split('\n').filter(Boolean).map(line => {
    const [hash, ...msg] = line.split(' ');
    return { hash, message: msg.join(' ') };
  });
}

function getCommitDiff(dir, hash) {
  try {
    return execSync(`git diff ${hash}^..${hash}`, { cwd: dir, encoding: 'utf-8', maxBuffer: 1024 * 1024 }).trim();
  } catch {
    // 可能是第一个提交
    try {
      return execSync(`git show ${hash}`, { cwd: dir, encoding: 'utf-8', maxBuffer: 1024 * 1024 }).trim();
    } catch { return ''; }
  }
}

function getChangedFiles(dir, since = 'HEAD~10') {
  try {
    const output = execSync(`git diff --name-only ${since}`, { cwd: dir, encoding: 'utf-8' }).trim();
    return output.split('\n').filter(Boolean);
  } catch { return []; }
}

function getRepoStructure(dir) {
  try {
    const output = execSync(`git ls-files --cached`, { cwd: dir, encoding: 'utf-8' }).trim();
    return output.split('\n').filter(Boolean).map(f => ({
      path: f,
      ext: path.extname(f),
      dir: path.dirname(f),
      name: path.basename(f),
      size: fs.existsSync(path.join(dir, f)) ? fs.statSync(path.join(dir, f)).size : 0,
    }));
  } catch { return []; }
}

function getActiveBranches(dir) {
  try {
    const output = execSync(`git branch -a`, { cwd: dir, encoding: 'utf-8' }).trim();
    return output.split('\n').filter(Boolean).map(b => b.trim().replace(/^\* /, ''));
  } catch { return []; }
}

// ========================================
// 索引操作
// ========================================

/**
 * 索引 git 仓库所有文件到知识库
 */
function indexRepo(kbName, repoPath) {
  guard();
  if (!isGitRepo(repoPath)) {
    throw new Error(`不是 Git 仓库: ${repoPath}`);
  }

  const root = getRoot(repoPath);
  const remote = getRemoteUrl(repoPath);
  const branch = getCurrentBranch(repoPath);
  const repoName = path.basename(root);

  const files = getRepoStructure(root);
  const totalFiles = files.length;

  // 先创建或获取知识库
  const { Storage } = getStorage();
  const store = new Storage(kbName || repoName);

  let indexed = 0;
  let skipped = 0;

  // 索引仓库元信息
  store.addDocument({
    title: `${repoName} — 仓库信息`,
    content: [
      `仓库: ${repoName}`,
      `路径: ${root}`,
      `分支: ${branch}`,
      `远程: ${remote || '无'}`,
      `文件数: ${totalFiles}`,
      `结构概览:\n${files.slice(0, 50).map(f => `  ${f.path}`).join('\n')}`,
    ].join('\n'),
    type: 'repo',
    tags: ['repo', repoName, 'meta'],
    source: root,
  });
  indexed++;

  // 按目录分组索引文件结构
  const dirMap = {};
  for (const file of files) {
    const dir = file.dir;
    if (!dirMap[dir]) dirMap[dir] = [];
    dirMap[dir].push(file);
  }

  for (const [dirPath, dirFiles] of Object.entries(dirMap)) {
    const dirName = dirPath || '/';
    const extensions = [...new Set(dirFiles.map(f => f.ext))];
    const langMap = {};
    for (const f of dirFiles) {
      const lang = f.ext.replace('.', '') || 'unknown';
      langMap[lang] = (langMap[lang] || 0) + 1;
    }
    const langSummary = Object.entries(langMap)
      .sort((a, b) => b[1] - a[1])
      .map(([lang, count]) => `${lang}: ${count}`)
      .join(', ');

    store.addDocument({
      title: `${repoName} — ${dirName || '/'}`,
      content: [
        `目录: ${dirName}`,
        `文件数: ${dirFiles.length}`,
        `语言分布: ${langSummary}`,
        `文件列表:\n${dirFiles.slice(0, 30).map(f => `  ${f.name} (${formatSize(f.size)})`).join('\n')}`,
      ].join('\n'),
      type: 'directory',
      tags: ['repo', repoName, 'dir', dirName.replace(/[/\\]/g, '-')],
      source: path.join(root, dirPath),
    });
    indexed++;
  }

  // 索引 README
  const readmeFiles = files.filter(f => /^readme/i.test(f.name));
  for (const readme of readmeFiles) {
    try {
      const content = fs.readFileSync(path.join(root, readme.path), 'utf-8');
      store.addDocument({
        title: `${repoName} — README`,
        content: content.substring(0, 8000),
        type: 'doc',
        tags: ['repo', repoName, 'readme'],
        source: path.join(root, readme.path),
      });
      indexed++;
    } catch {}
  }

  // 最近提交
  const commits = getRecentCommits(root, 30);
  for (const commit of commits) {
    const diff = getCommitDiff(root, commit.hash);
    if (diff) {
      // 提取 diff 统计
      const diffLines = diff.split('\n');
      const added = diffLines.filter(l => l.startsWith('+') && !l.startsWith('+++')).length;
      const removed = diffLines.filter(l => l.startsWith('-') && !l.startsWith('---')).length;
      const fileChanges = diff.split(/^diff --git /m).filter(Boolean).length - 1;

      store.addDocument({
        title: `${repoName} — ${commit.hash.substring(0, 8)}`,
        content: `提交: ${commit.hash}\n消息: ${commit.message}\n变更: ${fileChanges} 文件，+${added}/-${removed}\n\n${diff.substring(0, 4000)}`,
        type: 'commit',
        tags: ['repo', repoName, 'commit', commit.hash.substring(0, 8)],
        source: `${root} | ${commit.hash}`,
      });
      indexed++;
    }
  }

  store.close();
  return {
    kb: kbName || repoName,
    repo: repoName,
    branch,
    totalFiles,
    indexed,
    skipped,
  };
}

/**
 * 索引最近 N 次提交的变更
 */
function indexRecentChanges(kbName, repoPath, count = 10) {
  guard();
  if (!isGitRepo(repoPath)) throw new Error('不是 Git 仓库');

  const root = getRoot(repoPath);
  const repoName = path.basename(root);

  const { Storage } = getStorage();
  const store = new Storage(kbName || `${repoName}-changes`);

  const commits = getRecentCommits(root, count);
  let indexed = 0;

  for (const commit of commits) {
    const diff = getCommitDiff(root, commit.hash);
    const changedFiles = execSync(`git diff --name-only ${commit.hash}^..${commit.hash}`, { cwd: root, encoding: 'utf-8' }).trim().split('\n').filter(Boolean);

    store.addDocument({
      title: `变更: ${commit.hash.substring(0, 8)} ${commit.message}`,
      content: [
        `提交: ${commit.hash.substring(0, 12)}`,
        `消息: ${commit.message}`,
        `变更文件:\n${changedFiles.map(f => `  ${f}`).join('\n')}`,
        `\n---\n${diff.substring(0, 6000)}`,
      ].join('\n'),
      type: 'changeset',
      tags: ['changes', repoName, commit.hash.substring(0, 8)],
      source: `${root} | ${commit.hash}`,
    });
    indexed++;
  }

  store.close();
  return { kb: kbName || `${repoName}-changes`, count: indexed };
}

/**
 * 索引所有 git 仓库
 */
function indexAllRepos(reposDir) {
  const results = [];
  if (!fs.existsSync(reposDir)) return results;

  const entries = fs.readdirSync(reposDir);
  for (const entry of entries) {
    const fullPath = path.join(reposDir, entry);
    if (fs.statSync(fullPath).isDirectory() && isGitRepo(fullPath)) {
      try {
        const result = indexRepo(`repo-${entry}`, fullPath);
        results.push(result);
      } catch (e) {
        results.push({ repo: entry, error: e.message });
      }
    }
  }
  return results;
}

// ========================================
// 工具
// ========================================

function formatSize(bytes) {
  if (!bytes) return '0B';
  const sizes = ['B', 'KB', 'MB'];
  const i = Math.floor(Math.log(bytes) / Math.log(1024));
  return (bytes / Math.pow(1024, i)).toFixed(1) + sizes[i];
}

// ========================================
// CLI
// ========================================

async function cli() {
  const args = process.argv.slice(2);
  const cmd = args[0];

  switch (cmd) {
    case 'index':
      const kb = args[1] || undefined;
      const repo = args[2] || process.cwd();
      console.log(JSON.stringify(indexRepo(kb, repo), null, 2));
      break;

    case 'changes':
      const cKb = args[1] || undefined;
      const cRepo = args[2] || process.cwd();
      const count = parseInt(args[3] || '10', 10);
      console.log(JSON.stringify(indexRecentChanges(cKb, cRepo, count), null, 2));
      break;

    case 'info':
      const dir = args[1] || process.cwd();
      if (!isGitRepo(dir)) {
        console.log(JSON.stringify({ error: '不是 Git 仓库' }));
        break;
      }
      const root = getRoot(dir);
      console.log(JSON.stringify({
        root,
        remote: getRemoteUrl(dir),
        branch: getCurrentBranch(dir),
        branches: getActiveBranches(root),
        recentCommits: getRecentCommits(root, 5),
      }, null, 2));
      break;

    case 'scan':
      const scanDir = args[1] || process.cwd();
      if (!isGitRepo(scanDir)) {
        console.log(JSON.stringify({ error: '不是 Git 仓库' }));
        break;
      }
      const sRoot = getRoot(scanDir);
      const files = getRepoStructure(sRoot);
      const byExt = {};
      for (const f of files) {
        byExt[f.ext] = (byExt[f.ext] || 0) + 1;
      }
      console.log(JSON.stringify({
        root: sRoot,
        totalFiles: files.length,
        byExtension: byExt,
        dirs: [...new Set(files.map(f => f.dir))].length,
      }, null, 2));
      break;

    default:
      console.log('用法:');
      console.log('  node git.js index [知识库] [仓库路径]   — 索引整个仓库');
      console.log('  node git.js changes [知识库] [路径] [N] — 索引最近 N 次变更');
      console.log('  node git.js info [路径]                 — 仓库信息');
      console.log('  node git.js scan [路径]                 — 结构扫描');
      break;
  }
}

if (require.main === module) {
  cli();
}

module.exports = {
  indexRepo,
  indexRecentChanges,
  isGitRepo,
  getRoot,
  getRemoteUrl,
  getCurrentBranch,
  getRecentCommits,
  getRepoStructure,
};
