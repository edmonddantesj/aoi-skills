#!/usr/bin/env node
import fs from "fs";
import os from "os";
import path from "path";

const SCHEMA_VERSION = "aoi.squad.report.v0.1";
const ORCHESTRATOR_STATE_VERSION = 1;

const PRESETS = {
  "planner-builder-reviewer": {
    label: "Planner / Builder / Reviewer",
    roles: [
      { key: "planner", archetype: "Planner", objective: "Break the task into a simple plan with priorities and constraints." },
      { key: "builder", archetype: "Builder", objective: "Produce a concrete draft/implementation outline that follows the plan." },
      { key: "reviewer", archetype: "Reviewer", objective: "Review for correctness, risks, and missing steps; propose fixes." }
    ]
  },
  "researcher-writer-editor": {
    label: "Researcher / Writer / Editor",
    roles: [
      { key: "researcher", archetype: "Researcher", objective: "Collect assumptions and key facts; propose references to verify." },
      { key: "writer", archetype: "Writer", objective: "Write a clear, user-facing draft based on findings." },
      { key: "editor", archetype: "Editor", objective: "Improve clarity, structure, and consistency; remove fluff." }
    ]
  },
  "builder-security-operator": {
    label: "Builder / Security / Operator",
    roles: [
      { key: "builder", archetype: "Builder", objective: "Draft the build steps and command sequence (no external side effects)." },
      { key: "security", archetype: "Sentinel", objective: "Check for unsafe actions, secrets exposure, and policy violations." },
      { key: "operator", archetype: "Operator", objective: "Turn the result into a runnable checklist + VCP-style proof points." }
    ]
  }
};

const CALLSIGNS = [
  "Vega","Kestrel","Orion","Lyra","Atlas","Nova","Rune","Cobalt","Sable","Juniper",
  "Nimbus","Ash","Mosaic","Pulse","Quill","Beacon","Astra","Zenith","Hawke","Tundra"
];

function homeFile() {
  return path.join(os.homedir(), ".openclaw", "aoi", "squad_names.json");
}

function ensureDir(p) {
  fs.mkdirSync(path.dirname(p), { recursive: true });
}

function loadNames() {
  const fp = homeFile();
  try {
    const raw = fs.readFileSync(fp, "utf8");
    return JSON.parse(raw);
  } catch {
    return { schema: "aoi.squad.names.v0.1", presets: {} };
  }
}

function saveNames(db) {
  const fp = homeFile();
  ensureDir(fp);
  fs.writeFileSync(fp, JSON.stringify(db, null, 2) + "\n", "utf8");
}

function pickCallsign(used) {
  const available = CALLSIGNS.filter(c => !used.has(c));
  const arr = available.length ? available : CALLSIGNS;
  return arr[Math.floor(Math.random() * arr.length)];
}

function defaultName(archetype, used) {
  const cs = pickCallsign(used);
  used.add(cs);
  return `${archetype} ${cs}`;
}

function getOrInitTeam(db, preset) {
  if (!PRESETS[preset]) throw new Error(`Unknown preset: ${preset}`);
  db.presets[preset] ||= { roles: {} };
  const used = new Set(Object.values(db.presets[preset].roles || {}).map(x => x.split(" ").slice(1).join(" ")).filter(Boolean));

  for (const r of PRESETS[preset].roles) {
    if (!db.presets[preset].roles[r.key]) {
      db.presets[preset].roles[r.key] = defaultName(r.archetype, used);
    }
  }
  return db.presets[preset].roles;
}

function parseArgs(argv) {
  const out = { _: [] };
  for (let i = 0; i < argv.length; i++) {
    const a = argv[i];
    if (a.startsWith("--")) {
      const [k, v] = a.includes("=") ? a.slice(2).split("=") : [a.slice(2), argv[i + 1]];
      if (!a.includes("=")) i++;
      out[k] = v;
    } else {
      out._.push(a);
    }
  }
  return out;
}

function jsonOut(obj, code = 0) {
  process.stdout.write(JSON.stringify(obj, null, 2) + "\n");
  process.exit(code);
}

function fail(message, extra = {}) {
  jsonOut({ ok: false, error: message, ...extra }, 1);
}

function cmdPresetList() {
  const items = Object.entries(PRESETS).map(([key, p]) => ({ preset: key, label: p.label, roles: p.roles.map(r => r.key) }));
  jsonOut({ ok: true, presets: items });
}

function cmdTeamShow(args) {
  const preset = args.preset;
  if (!preset) return fail("Missing --preset");
  const db = loadNames();
  const roles = getOrInitTeam(db, preset);
  saveNames(db);
  jsonOut({ ok: true, preset, team: roles, file: homeFile() });
}

function validateName(name) {
  if (!name || typeof name !== "string") return "Name must be a string";
  if (name.length < 3 || name.length > 40) return "Name length must be 3..40";
  const bad = ["http://","https://","/","\\","://",".env","$", "~"];
  if (bad.some(b => name.includes(b))) return "Name contains disallowed characters";
  return null;
}

function cmdTeamRename(args) {
  const { preset, role, name } = args;
  if (!preset) return fail("Missing --preset");
  if (!role) return fail("Missing --role");
  if (!name) return fail("Missing --name");
  if (!PRESETS[preset]) return fail(`Unknown preset: ${preset}`);
  const roleKeys = new Set(PRESETS[preset].roles.map(r => r.key));
  if (!roleKeys.has(role)) return fail(`Unknown role '${role}' for preset '${preset}'`);
  const err = validateName(name);
  if (err) return fail(err);

  const db = loadNames();
  getOrInitTeam(db, preset);
  db.presets[preset].roles[role] = name;
  saveNames(db);
  jsonOut({ ok: true, preset, role, name, file: homeFile() });
}

function nowIso() {
  return new Date().toISOString();
}

function makeRunId() {
  return `run_${Date.now()}`;
}

function makeEventId(suffix) {
  return `evt_${Date.now()}_${suffix}`;
}

function orchestratorRoot() {
  return path.join(os.homedir(), ".openclaw", "aoi", "squad_runtime");
}

function runtimeFile(preset, name) {
  return path.join(orchestratorRoot(), preset, name);
}

function ensureRuntimeDir(preset) {
  fs.mkdirSync(path.join(orchestratorRoot(), preset), { recursive: true });
}

function writeJson(file, obj) {
  ensureDir(file);
  fs.writeFileSync(file, JSON.stringify(obj, null, 2) + "\n", "utf8");
}

function appendJsonl(file, obj) {
  ensureDir(file);
  fs.appendFileSync(file, JSON.stringify(obj) + "\n", "utf8");
}

function createInitialOrchestratorState(runId, task) {
  const now = nowIso();
  return {
    version: ORCHESTRATOR_STATE_VERSION,
    revision: 1,
    updatedAt: now,
    runId,
    mode: "active",
    currentTurn: {
      turnId: "turn_1",
      owner: "planner",
      status: "in_progress",
      startedAt: now,
      lastProgressAt: now,
      deadlineAt: null,
      leaseVersion: 1
    },
    sharedContext: {
      goal: task,
      constraints: [],
      inputs: [task],
      artifacts: []
    },
    agents: {
      planner: { status: "active", lastSeenAt: now, lastTurnId: "turn_1" },
      executor: { status: "idle", lastSeenAt: null, lastTurnId: null },
      reviewer: { status: "idle", lastSeenAt: null, lastTurnId: null }
    },
    allocation: {
      strategy: "single-owner-per-turn",
      override: null
    },
    flags: {
      blocked: false,
      needsReview: false,
      handoffRequested: false
    },
    lastDecision: {
      selectedAgent: "planner",
      reason: "task_intake",
      at: now
    }
  };
}

function handoffState(state, from, to, reason) {
  const now = nowIso();
  const next = JSON.parse(JSON.stringify(state));
  next.revision += 1;
  next.updatedAt = now;
  next.currentTurn.owner = to;
  next.currentTurn.leaseVersion += 1;
  next.currentTurn.lastProgressAt = now;
  next.currentTurn.status = to === "reviewer" ? "in_review" : "in_progress";
  next.agents[from].status = "idle";
  next.agents[from].lastSeenAt = now;
  next.agents[from].lastTurnId = next.currentTurn.turnId;
  next.agents[to].status = "active";
  next.agents[to].lastSeenAt = now;
  next.agents[to].lastTurnId = next.currentTurn.turnId;
  next.flags.needsReview = to === "reviewer";
  next.lastDecision = { selectedAgent: to, reason, at: now };
  return next;
}

function closeState(state, summary) {
  const now = nowIso();
  const next = JSON.parse(JSON.stringify(state));
  next.revision += 1;
  next.updatedAt = now;
  next.mode = "idle";
  next.flags.blocked = false;
  next.flags.needsReview = false;
  next.flags.handoffRequested = false;
  next.lastDecision = { selectedAgent: "reviewer", reason: "turn_closed:approved", at: now };
  next.currentTurn = null;
  next.summary = summary;
  return next;
}

function runOrchestratorPreset(preset, task, teamNames) {
  ensureRuntimeDir(preset);
  const runId = makeRunId();
  const statePath = runtimeFile(preset, "state.json");
  const eventsPath = runtimeFile(preset, "events.jsonl");

  let state = createInitialOrchestratorState(runId, task);
  writeJson(statePath, state);
  appendJsonl(eventsPath, {
    eventId: makeEventId("run_started"),
    type: "run_started",
    at: nowIso(),
    runId,
    actor: "system",
    revision: state.revision,
    severity: "info",
    data: { preset }
  });

  const plannerName = teamNames.planner || teamNames.researcher || teamNames.builder;
  const executorKey = teamNames.executor ? "executor" : teamNames.writer ? "writer" : "builder";
  const reviewerKey = teamNames.reviewer ? "reviewer" : teamNames.editor ? "editor" : "operator";
  const executorName = teamNames[executorKey];
  const reviewerName = teamNames[reviewerKey];

  const outputs = [];
  outputs.push({ nickname: plannerName, role: "Planner", objective: "Interpret the task and set the plan.", output: `Plan established for: ${task}`, artifacts: [] });

  state = handoffState(state, "planner", "executor", "spec_ready");
  writeJson(statePath, state);
  appendJsonl(eventsPath, {
    eventId: makeEventId("handoff_executor"),
    type: "turn_handoff",
    at: nowIso(),
    runId,
    actor: "planner",
    turnId: "turn_1",
    revision: state.revision,
    severity: "info",
    data: { from: "planner", to: "executor", reason: "spec_ready" }
  });
  outputs.push({ nickname: executorName, role: "Executor", objective: "Produce the main draft.", output: `Drafted execution outline for: ${task}`, artifacts: [] });

  state = handoffState(state, "executor", "reviewer", "implementation_done");
  writeJson(statePath, state);
  appendJsonl(eventsPath, {
    eventId: makeEventId("handoff_reviewer"),
    type: "turn_handoff",
    at: nowIso(),
    runId,
    actor: "executor",
    turnId: "turn_1",
    revision: state.revision,
    severity: "info",
    data: { from: "executor", to: "reviewer", reason: "implementation_done" }
  });
  outputs.push({ nickname: reviewerName, role: "Reviewer", objective: "Review correctness and risks.", output: `Reviewed output for: ${task}`, artifacts: [] });

  state = closeState(state, `Completed preset '${preset}' on task: ${task}`);
  writeJson(statePath, state);
  appendJsonl(eventsPath, {
    eventId: makeEventId("turn_closed"),
    type: "turn_closed",
    at: nowIso(),
    runId,
    actor: "reviewer",
    turnId: "turn_1",
    revision: state.revision,
    severity: "info",
    data: { outcome: "approved", summary: state.summary }
  });

  return { runId, statePath, eventsPath, outputs, finalState: state };
}

function mdEscape(s) {
  return String(s ?? "").replace(/</g, "&lt;").replace(/>/g, "&gt;");
}

function cmdRun(args) {
  const preset = args.preset;
  const task = args.task || "";
  if (!preset) return fail("Missing --preset");
  if (!task) return fail("Missing --task");
  if (!PRESETS[preset]) return fail(`Unknown preset: ${preset}`);

  const db = loadNames();
  const teamNames = getOrInitTeam(db, preset);
  saveNames(db);

  const started = nowIso();
  const orchestration = runOrchestratorPreset(preset, task, teamNames);
  const ended = nowIso();
  const runId = orchestration.runId;

  const team = PRESETS[preset].roles.map(r => {
    const nickname = teamNames[r.key];
    const found = orchestration.outputs.find(o => o.nickname === nickname);
    return {
      nickname,
      role: r.archetype,
      objective: r.objective,
      output: found?.output || "(no output)",
      artifacts: found?.artifacts || []
    };
  });

  const oneLine = `Completed preset '${preset}' on task: ${task.slice(0, 80)}${task.length > 80 ? "…" : ""}`;

  const reportMarkdown = `# AOI Squad Report (v0.1)\n- Preset: ${mdEscape(preset)}\n- Run: ${mdEscape(runId)}\n- Time: ${mdEscape(started)} → ${mdEscape(ended)}\n- Runtime state: ${mdEscape(orchestration.statePath)}\n- Runtime events: ${mdEscape(orchestration.eventsPath)}\n\n## Task\n${mdEscape(task)}\n\n## Team outputs\n${team.map(m => `### ${mdEscape(m.nickname)} (${mdEscape(m.role)})\n- Objective: ${mdEscape(m.objective)}\n- Output: ${mdEscape(m.output)}\n`).join("\n")}\n## Synthesis\n- One-line: ${mdEscape(oneLine)}\n- Decision:\n  - Approved by reviewer\n- Risks:\n  - MVP orchestration only; reasoning payloads are placeholders\n- Next actions:\n  - [P1] Extend command coverage and richer artifacts\n- VCP Proof:\n  - state.json written\n  - events.jsonl appended\n`;

  const out = {
    ok: true,
    schema_version: SCHEMA_VERSION,
    run: {
      run_id: runId,
      preset,
      started_at: started,
      ended_at: ended,
      limits: {
        max_roles: 3,
        max_turns: 6,
        max_wall_time_sec: 180,
        max_tokens: 8000
      }
    },
    task: {
      title: task.split("\n")[0].slice(0, 120),
      input: task,
      constraints: []
    },
    team,
    synthesis: {
      one_line_summary: oneLine,
      decision: ["approved"],
      risks: ["MVP orchestration placeholders"],
      next_actions: [
        { action: "Extend command coverage and richer artifacts", owner: team[0].nickname, priority: "P1" }
      ],
      vcp_proof: [
        { kind: "file", path: orchestration.statePath },
        { kind: "file", path: orchestration.eventsPath }
      ]
    },
    report_markdown: reportMarkdown,
    meta: {
      notes: ["This run is now backed by local orchestrator runtime files."],
      warnings: []
    }
  };

  jsonOut(out);
}

function main() {
  const argv = process.argv.slice(2);
  const cmd = argv[0];
  const sub = argv[1];
  const args = parseArgs(argv.slice(1));

  try {
    if (cmd === "preset" && sub === "list") return cmdPresetList();
    if (cmd === "team" && sub === "show") return cmdTeamShow(args);
    if (cmd === "team" && sub === "rename") return cmdTeamRename(args);
    if (cmd === "run") return cmdRun(parseArgs(argv.slice(1)));

    return fail("Unknown command", {
      usage: [
        "aoi-squad preset list",
        "aoi-squad team show --preset <preset>",
        "aoi-squad team rename --preset <preset> --role <role> --name \"Name\"",
        "aoi-squad run --preset <preset> --task \"...\""
      ]
    });
  } catch (e) {
    return fail(e?.message || String(e));
  }
}

main();
