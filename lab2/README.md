# Lab2 — Telegram 回显机器人

## 用 Conda 创建并激活环境

### 第一次使用：创建环境

在项目根目录或 `lab2` 目录下执行：

```bash
cd lab2
conda env create -f environment.yml
```

### 每次使用：激活环境并运行

```bash
conda activate 7940-lab2
cd D:\workplace\comp7940-lab\lab2
python chatbot.py
```

若报错 `Run 'conda init' before 'conda activate'`：

1. 先执行一次：`conda init powershell`
2. **关闭当前终端并重新打开**（或新开一个 PowerShell 窗口），再执行上面的激活与运行命令。

不想重启终端时，可不激活环境，直接指定环境运行：

```bash
cd D:\workplace\comp7940-lab\lab2
conda run -n 7940-lab2 python chatbot.py
```

### 删除环境（可选）

```bash
conda env remove -n 7940-lab2
```

---

## 若不用 environment.yml，手动创建环境

```bash
conda create -n 7940-lab2 python=3.11 -y
conda activate 7940-lab2
cd lab2
pip install -r requirements.txt
python chatbot.py
```

---

## 运行前

在 `config.ini` 中填入从 [@BotFather](https://t.me/BotFather) 获取的 `ACCESS_TOKEN`。

---

## 故障排除：终端一打开就报“禁止运行脚本”

**原因：** `conda init powershell` 会在你的 PowerShell 配置文件 `profile.ps1` 里加入 conda 初始化代码。每次打开 Cursor 终端时，PowerShell 会尝试执行这个配置文件，但系统默认**禁止运行脚本**，所以出现红字报错。

**解决：** 允许当前用户运行本地脚本（只影响你自己，且本地脚本可运行、远程脚本需签名，相对安全）。

1. **以管理员身份**打开 PowerShell：开始菜单 → 搜 “PowerShell” → 右键 → “以管理员身份运行”。
2. 执行：
   ```powershell
   Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
   ```
3. 若提示确认，输入 `Y` 回车。
4. 关闭 Cursor 再重新打开，或新开一个终端，红字应消失，`conda activate` 也可用。

若电脑有组策略限制、无法修改执行策略，可**不依赖 profile**，每次运行 lab2 时用：

```powershell
cd D:\workplace\comp7940-lab\lab2
conda run -n 7940-lab2 python chatbot.py
```
