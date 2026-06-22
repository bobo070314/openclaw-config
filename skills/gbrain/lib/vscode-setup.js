#!/usr/bin/env node
/**
 * gbrain — 安装 VS Code / Cursor 扩展为 gbrain 集成
 * 
 * 创建 Code Extension 代码片段文件，注册 gbrain 为 VS Code/Cursor 任务。
 * 
 * 实际使用方式：
 *   1. 通过 "code" 命令打开文件
 *   2. 通过 Tasks API 注册
 *   3. 使用 Keybindings 快捷调用
 */

const fs = require('fs');
const path = require('path');

function installExtension() {
  const homeDir = process.env.USERPROFILE || process.env.HOME;
  const vscodeDir = path.join(homeDir, '.vscode');
  const cursorDir = path.join(homeDir, '.cursor');

  // VS Code 弹框脚本（可通过 command palette 执行任务）
  const tasks = {
    version: '2.0.0',
    tasks: [
      {
        label: 'gbrain: 搜索知识库',
        type: 'shell',
        command: 'node',
        args: [
          path.resolve(__dirname, '..', 'commands', 'search.js')
        ],
        presentation: { echo: true, reveal: 'always', panel: 'dedicated' },
        problemMatcher: [],
      },
      {
        label: 'gbrain: 索引当前项目',
        type: 'shell',
        command: 'node',
        args: [
          path.resolve(__dirname, '..', 'lib', 'ide.js'),
          'index',
          'code',
          '${workspaceFolder}'
        ],
        presentation: { echo: true, reveal: 'always', panel: 'dedicated' },
      },
      {
        label: 'gbrain: 扫描项目结构',
        type: 'shell',
        command: 'node',
        args: [
          path.resolve(__dirname, '..', 'lib', 'ide.js'),
          'scan',
          '${workspaceFolder}',
          '3'
        ],
        presentation: { echo: true, reveal: 'silent', panel: 'dedicated' },
      },
      {
        label: 'gbrain: 检查 Ollama 状态',
        type: 'shell',
        command: 'node',
        args: [
          path.resolve(__dirname, '..', 'lib', 'ollama.js'),
          'check'
        ],
        presentation: { echo: false, reveal: 'silent', panel: 'dedicated' },
      },
    ]
  };

  // 写入 .vscode/tasks.json (workspace 级别)
  // 也创建 .cursor/tasks.json 兼容
  let installed = [];

  for (const dir of [vscodeDir, cursorDir]) {
    const tasksPath = path.join(dir, 'tasks.json');
    try {
      if (fs.existsSync(dir) && fs.statSync(dir).isDirectory()) {
        let existing = {};
        if (fs.existsSync(tasksPath)) {
          existing = JSON.parse(fs.readFileSync(tasksPath, 'utf-8'));
          // 合并任务，去重
          const existingLabels = (existing.tasks || []).map(t => t.label);
          const newTasks = tasks.tasks.filter(t => !existingLabels.includes(t.label));
          existing.tasks = [...(existing.tasks || []), ...newTasks];
        } else {
          existing = tasks;
        }
        fs.writeFileSync(tasksPath, JSON.stringify(existing, null, 2));
        installed.push({ editor: path.basename(dir), tasksPath, count: tasks.tasks.length });
      }
    } catch (e) {
      console.error(`⚠ 写入 ${tasksPath} 失败:`, e.message);
    }
  }

  // 也创建 keybindings 片段
  console.log(JSON.stringify({ installed, tasks: tasks.tasks.map(t => t.label) }, null, 2));

  // 输出快捷使用指南
  if (installed.length > 0) {
    console.log('\n✅ gbrain IDE 集成已安装！');
    console.log('\n在 VS Code / Cursor 中:');
    console.log('  Cmd+Shift+P → "Tasks: Run Task" → 选择 gbrain 任务');
    console.log('\n或者直接在终端:');
    console.log('  cd <项目目录> && node skills/gbrain/lib/ide.js index code .');
  }
}

installExtension();
