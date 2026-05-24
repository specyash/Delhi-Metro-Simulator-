# 🚇🚄 // DELHI METRO : ROUTING ENGINE // 🚄🚇

> **"A deterministic transit routing system engineered from absolute first principles."**

[![Python](https://img.shields.io/badge/Python-3.x-blue?style=for-the-badge&logo=python&logoColor=white)](https://python.org)
[![Logic Design](https://img.shields.io/badge/Architecture-Logic_Design-ff69b4?style=for-the-badge&logo=circuitverse)](https://github.com)
[![Dependencies](https://img.shields.io/badge/Dependencies-ZERO-brightgreen?style=for-the-badge)](https://github.com)
[![Optimization](https://img.shields.io/badge/Optimization-Heuristic-orange?style=for-the-badge)](https://github.com)

---

## ⚡ WHAT IS THIS?

Forget bulky graph libraries. Forget generic pathfinding solutions. This is a bare-metal, highly optimized routing engine custom-built to simulate optimal travel across the Delhi Metro’s **Blue** and **Magenta** lines. 

It evaluates, it audits, and it finds the *absolute global minimum-time path*—all while navigating the chaotic real-world constraints of transit systems.

---

## 🔥 CORE ARCHITECTURE & FEATURES

### 🧠 1. Custom Pathfinding Logic (Zero Dependencies)
We didn't just import `networkx` and call it a day. 
* Architected a **multi-stage evaluation engine** from scratch.
* Dynamically audits interchange validity on the fly.
* Identifies line-membership and constructs mathematically valid paths **without a single external graph library**.

### ⏱️ 2. Heuristic Optimization
Every second counts. 
* Implemented a ruthless time-based comparison algorithm.
* Evaluates cumulative travel costs across multiple candidate routes.
* Achieves the **global minimum-time path** through direct, state-based comparison.

### 🛡️ 3. Bulletproof Edge Case Handling
Real transit systems break. This engine doesn't.
* Designed robust control flows to manage catastrophic scenarios.
* Handles **"last-train"** cutoffs and sudden **service unavailability**.
* Ensures 100% simulation accuracy under brutal real-world operational constraints.

---

## ⚙️ UNDER THE HOOD

```text
[ START ] 
   ⬇
[ MAP BLUE/MAGENTA LINES ] 
   ⬇
[ DYNAMIC INTERCHANGE AUDIT ] ⟷ [ EDGE CASE TRIGGER: Last Train? ]
   ⬇
[ HEURISTIC TIME-COST EVALUATION ]
   ⬇
[ RETURN GLOBAL MINIMUM PATH ]
   ⬇
[ END ]
