const { Telegraf } = require('telegraf');
const { Storage } = require('../../lib/storage');

// 从环境变量读取 token
const BOT_TOKEN = process.env.TELEGRAM_BOT_TOKEN || 'YOUR_BOT_TOKEN_HERE';

if (!BOT_TOKEN || BOT_TOKEN === 'YOUR_BOT_TOKEN_HERE') {
  console.error('[❌] TELEGRAM_BOT_TOKEN 未设置！请在 .env 中配置');
  process.exit(1);
}

const bot = new Telegraf(BOT_TOKEN);

// 命令：/search <query>
bot.command('search', async (ctx) => {
  const query = ctx.message.text.split(' ').slice(1).join(' ');
  if (!query.trim()) {
    return ctx.reply('❌ 请提供搜索关键词，例如：/search 知识库');
  }

  try {
    const store = new Storage('default'); // 使用默认知识库
    const results = await store.search(query);
    
    if (results.length === 0) {
      return ctx.reply('🔍 未找到匹配结果');
    }
    
    const reply = `✅ 找到 ${results.length} 条结果：\n\n` + 
      results.slice(0, 3).map((r, i) => 
        `【${i + 1}】${r.title}\n${r.content.substring(0, 80)}...\n得分：${r.score.toFixed(3)}\n\n`
      ).join('');
    
    await ctx.reply(reply);
  } catch (e) {
    console.error('[Telegram] 搜索失败:', e);
    await ctx.reply('⚠️ 搜索时发生错误，请稍后重试');
  }
});

// 启动 Bot
bot.launch();
console.log('[🤖] Telegram Bot 已启动，监听 /search 命令');

// 清理
process.once('SIGINT', () => bot.stop('SIGINT'));
process.once('SIGTERM', () => bot.stop('SIGTERM'));
