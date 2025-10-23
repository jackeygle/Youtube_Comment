# 部署指南

## 已完成的步骤 ✅

1. ✅ 创建了专业的 README.md 文件
2. ✅ 创建了 .gitignore 保护敏感信息
3. ✅ 创建了 requirements.txt 依赖文件
4. ✅ 初始化了 Git 仓库
5. ✅ 添加并提交了所有文件
6. ✅ 添加了远程仓库地址

## 需要你完成的步骤 🔧

### 方法 1: 使用 HTTPS（推荐）

使用 GitHub 个人访问令牌（Personal Access Token）：

1. **创建个人访问令牌**：
   - 访问 https://github.com/settings/tokens
   - 点击 "Generate new token" → "Generate new token (classic)"
   - 选择权限：勾选 `repo` (全部子选项)
   - 点击 "Generate token"
   - **复制令牌**（只显示一次！）

2. **推送代码**：
   ```bash
   cd /Users/xinle/PycharmProjects/YouTubecomment
   git push -u origin main
   ```
   - 当提示输入用户名时，输入你的 GitHub 用户名：`jackeygle`
   - 当提示输入密码时，粘贴你刚才复制的个人访问令牌（不是 GitHub 密码！）

### 方法 2: 使用 SSH（适合长期使用）

1. **生成 SSH 密钥**（如果还没有）：
   ```bash
   ssh-keygen -t ed25519 -C "your_email@example.com"
   # 按 Enter 使用默认位置
   # 可以设置密码或直接按 Enter
   ```

2. **添加 SSH 密钥到 GitHub**：
   ```bash
   # 复制公钥
   cat ~/.ssh/id_ed25519.pub
   # 然后复制输出的内容
   ```
   - 访问 https://github.com/settings/keys
   - 点击 "New SSH key"
   - 粘贴公钥内容
   - 点击 "Add SSH key"

3. **修改远程仓库地址为 SSH**：
   ```bash
   cd /Users/xinle/PycharmProjects/YouTubecomment
   git remote set-url origin git@github.com:jackeygle/Youtube_Comment.git
   ```

4. **推送代码**：
   ```bash
   git push -u origin main
   ```

### 方法 3: 使用 GitHub CLI（最简单）

1. **安装 GitHub CLI**（如果还没有）：
   ```bash
   brew install gh
   ```

2. **登录**：
   ```bash
   gh auth login
   # 选择 GitHub.com
   # 选择 HTTPS
   # 按提示完成认证
   ```

3. **推送代码**：
   ```bash
   cd /Users/xinle/PycharmProjects/YouTubecomment
   git push -u origin main
   ```

## 验证部署成功 ✨

推送成功后，访问以下地址查看你的项目：
https://github.com/jackeygle/Youtube_Comment

你应该能看到：
- README.md 在仓库首页显示
- 所有代码文件都已上传
- .gitignore 生效，敏感文件未上传

## 后续维护

### 更新代码

```bash
cd /Users/xinle/PycharmProjects/YouTubecomment

# 查看修改
git status

# 添加修改的文件
git add .

# 提交更改
git commit -m "描述你的修改"

# 推送到 GitHub
git push
```

### 保护敏感信息

**重要提醒**：在推送代码前，请务必检查：

1. API 密钥是否已从代码中移除
2. credentials/ 文件夹是否在 .gitignore 中
3. token.pickle 等敏感文件是否被排除

如果不小心推送了敏感信息：
```bash
# 从历史记录中移除
git filter-branch --force --index-filter \
  "git rm --cached --ignore-unmatch config/settings.py" \
  --prune-empty --tag-name-filter cat -- --all

# 强制推送（谨慎使用）
git push origin --force --all
```

## 项目配置示例

为了安全，建议创建 `config/settings_local.py`（不上传到 Git）：

```python
# config/settings_local.py
GEMINI_API_KEY = "your_actual_api_key_here"
OPENAI_API_KEY = "your_openai_key_here"
CHANNEL_ID = "your_channel_id_here"
```

然后在 `config/settings.py` 中导入：

```python
try:
    from .settings_local import *
except ImportError:
    pass
```

## 需要帮助？

如果遇到问题：
1. 检查 GitHub 文档：https://docs.github.com/
2. 查看 Git 教程：https://git-scm.com/doc
3. 搜索错误信息

---

祝你使用愉快！🎉

