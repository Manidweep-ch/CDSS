# 🚀 Git Quick Reference - CDSS Team

## 📋 Daily Workflow (Copy & Paste)

### Start Work
```bash
git checkout main
git pull origin main
git checkout -b feature/your-feature-name
```

### Save Work
```bash
git add .
git commit -m "Add: description of what you did"
git push origin feature/your-feature-name
```

### After PR Merged
```bash
git checkout main
git pull origin main
git branch -d feature/your-feature-name
```

---

## 🔧 Common Commands

| Task | Command |
|------|---------|
| See status | `git status` |
| See branches | `git branch` |
| Switch branch | `git checkout branch-name` |
| Update main | `git pull origin main` |
| See history | `git log --oneline` |
| Undo changes | `git checkout -- filename` |

---

## 📝 Commit Message Format

```
Add: New feature
Fix: Bug description
Update: Improvement description
Docs: Documentation changes
Refactor: Code cleanup
```

---

## 🌿 Branch Naming

```
feature/liver-model
fix/pdf-bug
ui/dashboard-redesign
docs/update-readme
model/improve-diabetes
```

---

## ⚠️ Rules

1. ❌ Never work on `main` directly
2. ✅ Always pull before creating branch
3. ✅ Create PR for all changes
4. ✅ Get 1 approval before merging
5. ✅ Communicate with team

---

## 🆘 Emergency Commands

### Undo last commit (not pushed)
```bash
git reset --soft HEAD~1
```

### Discard all local changes
```bash
git checkout .
```

### Update branch with latest main
```bash
git checkout feature/your-branch
git merge main
```

---

## 📞 Who to Ask

- **Git problems**: Team Lead (Member 1)
- **Merge conflicts**: Person who wrote the code
- **Code review**: Any team member
- **Deployment**: Team Lead (Member 1)

---

**Keep this handy! 📌**
