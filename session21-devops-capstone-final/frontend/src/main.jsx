import { useEffect, useMemo, useState } from "react";
import { createRoot } from "react-dom/client";
import "./styles.css";

const emptyTask = { title: "", description: "", status: "todo", priority: "medium", owner: "Saranya" };
const statusName = { todo: "To do", in_progress: "In progress", done: "Done" };

function App() {
  const [tasks, setTasks] = useState([]);
  const [stats, setStats] = useState({ total: 0, todo: 0, in_progress: 0, done: 0 });
  const [filter, setFilter] = useState("all");
  const [showModal, setShowModal] = useState(false);
  const [form, setForm] = useState(emptyTask);
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(true);

  async function load() {
    setLoading(true); setError("");
    try {
      const [taskResponse, statsResponse] = await Promise.all([fetch("/api/tasks"), fetch("/api/tasks/stats")]);
      if (!taskResponse.ok || !statsResponse.ok) throw new Error("The API did not respond successfully.");
      setTasks(await taskResponse.json()); setStats(await statsResponse.json());
    } catch (err) { setError("ProjectPulse cannot reach the backend. Start Docker Compose and refresh."); }
    finally { setLoading(false); }
  }
  useEffect(() => { load(); }, []);
  const visibleTasks = useMemo(() => filter === "all" ? tasks : tasks.filter((task) => task.status === filter), [tasks, filter]);
  async function createTask(event) {
    event.preventDefault();
    const response = await fetch("/api/tasks", { method: "POST", headers: { "Content-Type": "application/json" }, body: JSON.stringify(form) });
    if (!response.ok) { setError("Task could not be saved. Check required fields."); return; }
    setForm(emptyTask); setShowModal(false); load();
  }
  async function advance(task) {
    const next = task.status === "todo" ? "in_progress" : task.status === "in_progress" ? "done" : "todo";
    await fetch(`/api/tasks/${task.id}`, { method: "PUT", headers: { "Content-Type": "application/json" }, body: JSON.stringify({ status: next }) });
    load();
  }
  return <div className="shell">
    <aside><div className="brand">◆ ProjectPulse</div><p className="workspace">WORKSPACE</p><nav><a className="active">▦ Overview</a><a>✓ My tasks</a><a>◌ Timeline</a><a>▤ Reports</a></nav><div className="aside-bottom"><span className="avatar">ST</span><span>Saranya Tavva<br/><small>Engineering</small></span></div></aside>
    <main><header><div><p className="eyebrow">MONDAY, 15 OCTOBER</p><h1>Good morning, Saranya <span>✦</span></h1><p className="muted">Here is the delivery pulse across your workspace.</p></div><button onClick={() => setShowModal(true)}>+ Create task</button></header>
    {error && <div className="error">{error}</div>}
    <section className="kpis"><Kpi label="Total tasks" value={stats.total} icon="▣"/><Kpi label="In progress" value={stats.in_progress} icon="↗"/><Kpi label="Completed" value={stats.done} icon="✓"/><Kpi label="Delivery health" value={stats.total ? `${Math.round((stats.done / stats.total) * 100)}%` : "—"} icon="♥"/></section>
    <section className="panel"><div className="panel-head"><div><h2>Delivery board</h2><p>Prioritize the work that moves the release forward.</p></div><div className="filters">{["all", "todo", "in_progress", "done"].map((name) => <button className={filter === name ? "filter selected" : "filter"} onClick={() => setFilter(name)} key={name}>{name === "all" ? "All" : statusName[name]}</button>)}</div></div>
      <div className="table-wrap"><table><thead><tr><th>Task</th><th>Owner</th><th>Priority</th><th>Status</th><th></th></tr></thead><tbody>{loading ? <tr><td colSpan="5" className="center">Loading project data…</td></tr> : visibleTasks.length ? visibleTasks.map((task) => <tr key={task.id}><td><strong>{task.title}</strong><small>{task.description || "No description"}</small></td><td>{task.owner}</td><td><span className={`badge ${task.priority}`}>{task.priority}</span></td><td><span className={`status ${task.status}`}>{statusName[task.status]}</span></td><td><button className="advance" onClick={() => advance(task)}>Advance →</button></td></tr>) : <tr><td colSpan="5" className="center">No tasks in this view. Create one to start the board.</td></tr>}</tbody></table></div></section>
    <section className="bottom-grid"><div className="panel activity"><h2>Recent activity</h2><p><b>●</b> API health, readiness, and Prometheus metrics are enabled.</p><p><b>●</b> CI validates tests before an image can be published.</p><p><b>●</b> Helm deployment supports safe, repeatable releases.</p></div><div className="panel pipeline"><h2>Release pipeline</h2><div className="steps"><span>Code</span><i></i><span>Test</span><i></i><span>Scan</span><i></i><span>Deploy</span><i></i><span>Observe</span></div><p>Commit SHA tags connect source, images, and deployment history.</p></div></section></main>
    {showModal && <div className="modal-backdrop"><form className="modal" onSubmit={createTask}><div className="modal-head"><h2>Create a task</h2><button type="button" className="close" onClick={() => setShowModal(false)}>×</button></div><label>Task title<input required minLength="2" value={form.title} onChange={(e) => setForm({...form, title:e.target.value})}/></label><label>Description<textarea value={form.description} onChange={(e) => setForm({...form, description:e.target.value})}/></label><div className="form-grid"><label>Owner<input value={form.owner} onChange={(e) => setForm({...form, owner:e.target.value})}/></label><label>Priority<select value={form.priority} onChange={(e) => setForm({...form, priority:e.target.value})}>{["low","medium","high","critical"].map(x=><option key={x}>{x}</option>)}</select></label></div><button type="submit">Add to board</button></form></div>}
  </div>;
}
function Kpi({ label, value, icon }) { return <article className="kpi"><span>{icon}</span><p>{label}</p><strong>{value}</strong><small>Live from API</small></article>; }
createRoot(document.getElementById("root")).render(<App />);
