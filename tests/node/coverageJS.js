// coverageJS.js

const STOPWORDS = new Set(["a","an","the","is","are","of","to","your","my","our","their","his","her","there","this","that","what"]);

function normalize(text) {
  text = text.toLowerCase().replace(/[^\w\s]/g, " ");
  return text.split(/\s+/).filter(t => t && !STOPWORDS.has(t));
}

function tokenOverlapScore(question, transcript) {
  const q = new Set(normalize(question));
  if (q.size === 0) return 0.0;
  const t = new Set(normalize(transcript));
  let overlap = 0;
  q.forEach(tok => { if (t.has(tok)) overlap++; });
  return overlap / q.size;
}

function checkCoverage(transcript, requiredQuestions, threshold = 0.6) {
  const asked = [];
  const missed = [];
  for (const q of requiredQuestions) {
    const score = tokenOverlapScore(q, transcript);
    const rec = { question: q, match_score: Math.round(score * 100) / 100 };
    if (score >= threshold) asked.push(rec); else missed.push(rec);
  }
  const coverage = Math.round((asked.length / Math.max(1, requiredQuestions.length)) * 100) / 100;
  return { asked, missed, coverage };
}

module.exports = { checkCoverage };
