# Python Turn-Based Battle Game

A console (CLI) turn-based battle game built in Python emphasizing object-oriented design, modular actions, and extensible combat mechanics.

---

## 📌 Features
- Turn based combat with alternating turns.
- Speed determines turn order.
- Critical hit system.
- Stamina system with recovery each turn.
- Multiple actions(attack, defend, power attack).
- Modular action architecture - easy to extend.
- Enemy AI uses action choices.

---

## 🧱 Architecture

This project demonstrates a clean, extensible design pattern:

- **Character Class**: Holds  stats, current state, and available actions.
- **Action Base Class + Subclasses**: Attack, PowerAttack, Defend, Hesitate.
- **BattleEngine**: Orchestrates turn logic, action execution, and stamina recovery.

Designed to follow the *Open-Closed Principle* - adding new actions does not require modifying engine logic.

---

## 🎮 Example Usage

Run from terminal:

```bash
python turn_based_battle_game.py
```

## 🖥 Example Output

--- Turn 1 ---
Knight attacks Goblin for 10 damage!
Goblin attacks Knight for 5 damage!
Knight: 95/100, Stamina: 100/100
Goblin: 50/60, Stamina: 100/100

--- Turn 2 ---
Knight uses PowerAttack on Goblin for 22 damage!
Goblin hesitates!
Knight: 95/100, Stamina: 70/100
Goblin: 28/60, Stamina: 100/100

--- Turn 3 ---
Knight attacks Goblin for 11 damage!
Goblin uses PowerAttack on Knight for 18 damage!
Knight: 77/100, Stamina: 70/100
Goblin: 17/60, Stamina: 70/100

--- Battle Finished ---
Player wins!

---

## ⚙️ Requirements

- Python 3.8+
- Standard library only (no external dependencies)

---

## 🚀 How to Extend

- Add new **Action** subclasses to introduce more abilities.
- Modify **enemy_decide** in `BattleEngine` to implement smarter AI.
- Adjust **Character** stats for balancing different difficulty levels.
