# slowloris.py - Simple slowloris in Python

> ⚠️ **Educational Use Only!** This script is for learning and research purposes only. Do not use on unauthorized systems.

---

## 💀 Modified & Maintained by: `Z.A.I.` (Zain)

Original Author: [Gokberk Yaltirakli](https://github.com/gkbrk/slowloris)  
Modified & Improved by: **Z.A.I.**  
Year: **2025**  

---

## 🐍 What is Slowloris?
Slowloris is an HTTP Denial of Service attack that targets threaded servers. Here's how it works:

1. Multiple HTTP requests are initiated.
2. Headers are sent periodically (~15 seconds) to keep connections alive.
3. Connections are never closed unless the server closes them.

This fills up the server’s thread pool, making it unresponsive to legit user.
