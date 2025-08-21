def apply_physics(state: dict, action: dict):
    user_id = action["user_id"]
    if user_id not in state["players"]:
        state["players"][user_id] = {"x": 400, "y": 300, "vx": 0, "vy": 0}
    
    p = state["players"][user_id]

    speed = 0.5
    friction = 0.9

    if action["action_type"] == "left":
        p["vx"] = max(p["vx"] - speed, -5)
    elif action["action_type"] == "right":
        p["vx"] = min(p["vx"] + speed, 5)
    elif action["action_type"] == "up":
        p["vy"] = max(p["vy"] - speed, -5)
    elif action["action_type"] == "down":
        p["vy"] = min(p["vy"] + speed, 5)

    p["vx"] *= friction
    p["vy"] *= friction

    p["x"] += p["vx"]
    p["y"] += p["vy"]

    p["x"] = max(0, min(800, p["x"]))
    p["y"] = max(0, min(600, p["y"]))

    return {
        "players": {
            user_id: {"x": p["x"], "y": p["y"], "vx": p["vx"], "vy": p["y"]}
        }
    }
