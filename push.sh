#!/bin/bash
# YouTube Comment Bot - GitHub 推送脚本

echo "======================================"
echo "  YouTube Comment Bot - 推送到 GitHub"
echo "======================================"
echo ""

cd /Users/xinle/PycharmProjects/YouTubecomment

# 显示当前状态
echo "📊 当前 Git 状态："
git status
echo ""

echo "📝 准备推送的提交："
git log --oneline -6
echo ""

echo "🔍 检查敏感文件是否被排除："
if git ls-files | grep -q "settings_local.py"; then
    echo "❌ 警告：settings_local.py 在上传列表中！"
    exit 1
else
    echo "✅ settings_local.py 已被排除"
fi

if git ls-files | grep -q "credentials/"; then
    echo "❌ 警告：credentials/ 在上传列表中！"
    exit 1
else
    echo "✅ credentials/ 已被排除"
fi

if git ls-files | grep -q "token.pickle"; then
    echo "❌ 警告：token.pickle 在上传列表中！"
    exit 1
else
    echo "✅ token.pickle 已被排除"
fi

echo ""
echo "======================================"
echo "准备推送到："
git remote -v | grep push
echo "======================================"
echo ""
echo "⚠️  需要 GitHub 认证"
echo ""
echo "请选择认证方式："
echo "1. 个人访问令牌（推荐）"
echo "2. SSH 密钥"
echo ""
echo "方式 1: 个人访问令牌"
echo "-----------------------------------"
echo "如果还没有令牌，请访问："
echo "https://github.com/settings/tokens/new"
echo ""
echo "勾选 'repo' 权限，生成令牌后复制"
echo ""
echo "准备好后，执行推送..."
echo ""

# 推送
git push -u origin main

if [ $? -eq 0 ]; then
    echo ""
    echo "======================================"
    echo "🎉 推送成功！"
    echo "======================================"
    echo ""
    echo "访问你的仓库："
    echo "https://github.com/jackeygle/Youtube_Comment"
    echo ""
else
    echo ""
    echo "======================================"
    echo "❌ 推送失败"
    echo "======================================"
    echo ""
    echo "常见问题："
    echo "1. 确保使用个人访问令牌，不是 GitHub 密码"
    echo "2. 令牌需要有 'repo' 权限"
    echo "3. 用户名：jackeygle"
    echo ""
    echo "或者使用 SSH："
    echo "git remote set-url origin git@github.com:jackeygle/Youtube_Comment.git"
    echo "git push -u origin main"
fi

