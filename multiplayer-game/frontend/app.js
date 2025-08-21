let ws;
const state = { players: {} };

function connect() {
  const token = "fake-jwt-token"; // later: from login
  ws = new WebSocket(`ws://localhost:8000/api/v1/rooms/ws/1?token=${token}`);

  ws.onopen = () => {
    console.log("Connected");
    ws.send(JSON.stringify({ type: "join" }));
  };

  ws.onmessage = (e) => {
    const msg = JSON.parse(e.data);
    if (msg.type === "player_action") {
      const { user_id, action } = msg.payload;
      if (!state.players[user_id]) state.players[user_id] = { x: 400, y: 300 };
      if (action === "left") state.players[user_id].x -= 5;
      if (action === "right") state.players[user_id].x += 5;
      if (action === "up") state.players[user_id].y -= 5;
      if (action === "down") state.players[user_id].y += 5;
      canvas.render(state);
    }
  };

  document.addEventListener("keydown", (e) => {
    const map = { ArrowLeft: "left", ArrowRight: "right", ArrowUp: "up", ArrowDown: "down" };
    if (map[e.key]) {
      e.preventDefault();
      ws.send(JSON.stringify({ type: "action", payload: { action: map[e.key] } }));
    }
  });
}