# ⚠️ 安全警告

## 🚨 立即行动！

你的 `config/settings.py` 文件中包含了以下敏感信息：

1. **Gemini API Key**: `AIzaSyDI9n4W0yXt3hwT3AuJaF-DEhg2HggZH_s`
2. **OpenAI API Key**: 开头为 `sk-proj-FowTYDAGov3ECt9ozksfh127...`

**这些密钥已经在代码中暴露，在推送到 GitHub 之前必须处理！**

## 🔒 解决方案

### 选项 1：移除密钥后再推送（推荐）

1. **修改 `config/settings.py`**，将所有 API 密钥替换为环境变量：

```python
# config/settings.py
import os

# 使用环境变量
GEMINI_API_KEY = os.getenv('GEMINI_API_KEY', '')
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY', '')
CHANNEL_ID = os.getenv('YOUTUBE_CHANNEL_ID', '')
```

2. **创建 `config/settings_local.py`**（此文件不会上传到 Git）：

```python
# config/settings_local.py
GEMINI_API_KEY = "AIzaSyDI9n4W0yXt3hwT3AuJaF-DEhg2HggZH_s"
OPENAI_API_KEY = "sk-proj-FowTYDAGov3ECt9ozksfh127..."
CHANNEL_ID = "UCMxlvqb3ZW7d9eUki3WMw8A"
```

3. **在 `config/settings.py` 末尾添加**：

```python
# 导入本地配置（如果存在）
try:
    from .settings_local import *
except ImportError:
    pass
```

4. **重新提交更改**：

```bash
cd /Users/xinle/PycharmProjects/YouTubecomment
git add config/settings.py
git commit -m "Remove sensitive API keys from settings.py"
```

### 选项 2：使用环境变量

创建一个 `.env` 文件（此文件不会上传到 Git）：

```bash
# .env
GEMINI_API_KEY=AIzaSyDI9n4W0yXt3hwT3AuJaF-DEhg2HggZH_s
OPENAI_API_KEY=sk-proj-FowTYDAGov3ECt9ozksfh127...
YOUTUBE_CHANNEL_ID=UCMxlvqb3ZW7d9eUki3WMw8A
```

然后在运行程序前加载这些环境变量：

```bash
export GEMINI_API_KEY=AIzaSyDI9n4W0yXt3hwT3AuJaF-DEhg2HggZH_s
export OPENAI_API_KEY=sk-proj-FowTYDAGov3ECt9ozksfh127...
export YOUTUBE_CHANNEL_ID=UCMxlvqb3ZW7d9eUki3WMw8A

python main.py
```

## 🔐 如果密钥已经泄露

如果你已经将包含密钥的代码推送到了 GitHub：

1. **立即撤销所有 API 密钥**：
   - Google Gemini: https://makersuite.google.com/app/apikey
   - OpenAI: https://platform.openai.com/api-keys

2. **生成新的 API 密钥**

3. **清理 Git 历史**（可选，但推荐）：

```bash
# 从所有历史记录中移除文件
git filter-branch --force --index-filter \
  "git rm --cached --ignore-unmatch config/settings.py" \
  --prune-empty --tag-name-filter cat -- --all

# 强制推送（会覆盖远程历史）
git push origin --force --all
```

## ✅ 推送前检查清单

在执行 `git push` 之前，确保：

- [ ] `config/settings.py` 中没有实际的 API 密钥
- [ ] 敏感信息已移至 `settings_local.py` 或环境变量
- [ ] `.gitignore` 包含 `config/settings_local.py`
- [ ] `.gitignore` 包含 `.env`
- [ ] `credentials/` 文件夹被 `.gitignore` 排除
- [ ] `token.pickle` 被 `.gitignore` 排除

## 📚 最佳实践

1. **永远不要**将 API 密钥、密码或令牌提交到版本控制
2. 使用环境变量或配置文件（添加到 `.gitignore`）
3. 定期轮换 API 密钥
4. 为不同的项目使用不同的 API 密钥
5. 监控 API 密钥的使用情况

## 🆘 需要帮助？

如果你不确定如何处理，请：
1. **暂时不要推送到 GitHub**
2. 先完成上述安全措施
3. 确认无误后再推送

---

**记住：一旦代码推送到 GitHub，即使后来删除，API 密钥也可能已经被他人获取。请务必撤销并重新生成密钥。**

