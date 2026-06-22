// gbrain: query knowledge
const { search } = require('../lib/storage');

module.exports = async function query(args) {
  const { q } = args;
  if (!q) throw new Error('Query required');

  const results = await search(q);
  return {
    success: true,
    results: results.map(r => ({
      title: r.title,
      content: r.content.substring(0, 200),
      score: r.score,
      source: r.source
    }))
  };
}