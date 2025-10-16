// testCoverageJS.js

// cd to tests/node
// Run: node testCoverageJS.js

const fs = require("fs");
const path = require("path");
const { checkCoverage } = require("./coverageJS");

const BASE = __dirname;                      // .../tests/node
const TESTS_DIR = path.resolve(BASE, "..");  // .../tests
const SAMPLE = path.join(TESTS_DIR, "sample_data");

function read(p) { return fs.readFileSync(p, "utf-8"); }
function ensure(p) { if (!fs.existsSync(p)) throw new Error("Missing file: " + p); }

const rqPath  = path.join(SAMPLE, "required_questions.json");
const posPath = path.join(SAMPLE, "transcript_positive.txt");
const negPath = path.join(SAMPLE, "transcript_negative.txt");
[ rqPath, posPath, negPath ].forEach(ensure);

const rq = JSON.parse(read(rqPath));
const required = rq.required;
const threshold = Number(rq.threshold ?? 0.6);

const pos = read(posPath).trim();
const neg = read(negPath).trim();
if (pos === neg) throw new Error("Positive and negative transcripts are IDENTICAL. Fix tests/sample_data/*.txt.");

function runCase(name, transcriptLabel, transcriptText, required, threshold, expectAsked, expectCoverage) {
  console.log(`\n===== CASE: ${name} =====`);
  console.log(`--- Transcript (${transcriptLabel}) ---`);
  console.log(transcriptText);
  console.log("---------------------------------------");

  const res = checkCoverage(transcriptText, required, threshold);
  const passed = (res.asked.length === expectAsked) && (Math.abs(res.coverage - expectCoverage) < 1e-9);
  const status = passed ? "PASS" : "FAIL";
  console.log(`[${status}] ${name}`);
  console.log("  asked:");  res.asked.forEach(a => console.log(`    - ${a.question} (score=${a.match_score})`));
  console.log("  missed:"); res.missed.forEach(m => console.log(`    - ${m.question} (score=${m.match_score})`));
  console.log(`  coverage=${res.coverage}`);
  console.log("\n");
  return passed;
}

let total = 0, ok = 0;
total++; if (runCase("All detected", "positive", pos, required, threshold, 3, 1.0)) ok++;
total++; if (runCase("None detected", "negative", neg, required, threshold, 0, 0.0)) ok++;
console.log(`\nRESULT: ${ok}/${total} tests passed.`);
