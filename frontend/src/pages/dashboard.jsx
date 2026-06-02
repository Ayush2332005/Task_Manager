import { useEffect, useState } from "react";
import api from "../services/api";

function Dashboard() {
  const [title, setTitle] = useState("");
  const [tasks, setTasks] = useState([]);

  const getTasks = async () => {
    try {
      const response = await api.get("/tasks");

      setTasks(response.data);
    } catch (error) {
      console.log(error);
    }
  };

  useEffect(() => {
    getTasks();
  }, []);

  const addTask = async () => {
    try {
      await api.post("/tasks", {
        title,
      });

      setTitle("");
      getTasks();
    } catch (error) {
      console.log(error);
    }
  };

  const deleteTask = async (id) => {
    try {
      await api.delete(`/tasks/${id}`);

      getTasks();
    } catch (error) {
      console.log(error);
    }
  };

  const logout = () => {
    localStorage.removeItem("token");

    window.location.href = "/login";
  };

  return (
    <div>
      <h2>Task Dashboard</h2>

      <button onClick={logout}>
        Logout
      </button>

      <br /><br />

      <input
        placeholder="Task title"
        value={title}
        onChange={(e) =>
          setTitle(e.target.value)
        }
      />

      <button onClick={addTask}>
        Add Task
      </button>

      <hr />

      {tasks.map((task) => (
        <div key={task.id}>
          <h4>{task.title}</h4>

          <button
            onClick={() =>
              deleteTask(task.id)
            }
          >
            Delete
          </button>

          <hr />
        </div>
      ))}
    </div>
  );
}

export default Dashboard;