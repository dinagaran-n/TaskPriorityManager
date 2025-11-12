const apiBaseInput = document.getElementById("apiBase");
const tasksContainer = document.getElementById("tasksContainer");
const saveBtn = document.getElementById("saveTask");
const reloadBtn = document.getElementById("reload");

reloadBtn.addEventListener("click", loadTasks);
saveBtn.addEventListener("click", createTask);

async function loadTasks() {
  tasksContainer.innerHTML = "Loading...";
  try {
    const res = await fetch(`${apiBaseInput.value}/tasks`);
    if (!res.ok) throw new Error("Failed to load tasks");
    const data = await res.json();
    if (!Array.isArray(data) || data.length === 0) {
      tasksContainer.innerHTML = "<p>No tasks yet ✨</p>";
      return;
    }
    tasksContainer.innerHTML = data
      .map(
        (t) => `
      <div class="task">
        <h3>${t.title}</h3>
        <p>${t.description || ""}</p>
        <div class="meta">
          <span>Priority: ${t.priority}</span> |
          <span>Status: ${t.status}</span> |
          <span>Due: ${t.due_date || "—"}</span>
        </div>
      </div>`
      )
      .join("");
  } catch (err) {
    tasksContainer.innerHTML = `<p style="color:red">Error: ${err.message}</p>`;
  }
}

async function createTask() {
  const title = document.getElementById("title").value.trim();
  if (!title) {
    alert("Please enter a task title.");
    return;
  }

  const payload = {
    title,
    description: document.getElementById("description").value.trim(),
    priority: parseInt(document.getElementById("priority").value) || 3,
    status: document.getElementById("status").value,
    due_date: document.getElementById("due_date").value || null,
  };

  try {
    const res = await fetch(`${apiBaseInput.value}/tasks`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(payload),
    });
    if (!res.ok) throw new Error("Failed to create task");
    await loadTasks();
    document.querySelectorAll("input, textarea").forEach((el) => (el.value = ""));
  } catch (err) {
    alert(`Error: ${err.message}`);
  }
}

loadTasks();
