const canvas = document.getElementById("game");
const ctx = canvas.getContext("2d");

window.canvas = {
  render(state) {
    ctx.clearRect(0, 0, canvas.width, canvas.height);
    Object.entries(state.players).forEach(([id, p]) => {
      ctx.fillStyle = id.includes("guest") ? "gray" : "red";
      ctx.fillRect(p.x - 10, p.y - 10, 20, 20);
      ctx.fillText(id, p.x - 10, p.y - 15);
    });
  }
};