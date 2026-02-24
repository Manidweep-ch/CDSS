# 👥 Team Collaboration Guide - CDSS Project

## Team Size: 5 Members

This guide explains how to collaborate effectively on the CDSS project using Git and GitHub.

---

## 🎯 Workflow Overview

We use a **Branch-Based Workflow**:
- `main` branch = Production (always working)
- Feature branches = Individual work
- Pull Requests = Code review before merging

---

## 🚀 Initial Setup (One-Time)

### Step 1: Repository Owner (You) - Add Team Members

1. Go to: https://github.com/Manidweep-ch/CDSS
2. Click **Settings** → **Collaborators**
3. Click **Add people**
4. Add all 4 team members by username/email
5. Each member receives an invitation email

### Step 2: Team Members - Accept Invitation

1. Check email for GitHub invitation
2. Click **Accept invitation**
3. You now have access to the repository

### Step 3: Everyone - Clone Repository

```bash
git clone https://github.com/Manidweep-ch/CDSS.git
cd CDSS
```

### Step 4: Everyone - Configure Git

```bash
git config user.name "Your Name"
git config user.email "your.email@example.com"
```

---

## 📋 Team Roles & Responsibilities

### Suggested Division:

**Member 1 (You)** - Project Lead
- Merge pull requests
- Deploy to production
- Overall coordination

**Member 2** - ML Models
- Add new health panel models
- Improve existing models
- Model training scripts

**Member 3** - Backend API
- New API endpoints
- Database changes
- Backend features

**Member 4** - Frontend UI
- UI improvements
- New pages/components
- Styling

**Member 5** - Testing & Documentation
- Write tests
- Update documentation
- Bug fixes

---

## 🔄 Daily Workflow (Everyone Follows This)

### 1. Start Your Day - Get Latest Code

```bash
cd CDSS
git checkout main
git pull origin main
```

### 2. Create a Feature Branch

```bash
# Use descriptive branch names
git checkout -b feature/liver-model
# or
git checkout -b fix/pdf-extraction-bug
# or
git checkout -b ui/improve-dashboard
```

**Branch Naming Convention:**
- `feature/description` - New features
- `fix/description` - Bug fixes
- `ui/description` - UI changes
- `docs/description` - Documentation
- `model/description` - ML model work

### 3. Make Your Changes

```bash
# Edit files
# Test your changes locally
```

### 4. Commit Your Changes

```bash
git add .
git commit -m "Add: Liver function ML model with XGBoost"
```

**Commit Message Format:**
- `Add: description` - New feature
- `Fix: description` - Bug fix
- `Update: description` - Improvements
- `Docs: description` - Documentation
- `Refactor: description` - Code cleanup

### 5. Push Your Branch

```bash
git push origin feature/liver-model
```

### 6. Create Pull Request

1. Go to GitHub repository
2. Click **"Compare & pull request"** (appears after push)
3. Fill in:
   - **Title**: Clear description
   - **Description**: What you changed and why
   - **Reviewers**: Tag team members
4. Click **"Create pull request"**

### 7. Wait for Review

- Team members review your code
- Make changes if requested
- Once approved, project lead merges

### 8. After Merge - Update Your Local

```bash
git checkout main
git pull origin main
git branch -d feature/liver-model  # Delete old branch
```

---

## 👀 Code Review Process

### For Reviewers:

1. Go to **Pull Requests** tab
2. Click on the PR to review
3. Check:
   - ✅ Code works correctly
   - ✅ No bugs introduced
   - ✅ Follows project structure
   - ✅ Has clear commit messages
4. Leave comments or approve
5. Click **"Approve"** or **"Request changes"**

### For Project Lead (Merging):

1. Ensure PR is approved by at least 1 person
2. Check for conflicts
3. Click **"Merge pull request"**
4. Click **"Confirm merge"**
5. Delete the branch (GitHub prompts you)

---

## ⚠️ Handling Merge Conflicts

If your branch conflicts with main:

```bash
# Update your branch with latest main
git checkout main
git pull origin main
git checkout feature/your-branch
git merge main

# Fix conflicts in files
# Look for:
<<<<<<< HEAD
Your changes
=======
Main branch changes
>>>>>>> main

# Edit files to resolve
git add .
git commit -m "Merge: Resolve conflicts with main"
git push origin feature/your-branch
```

---

## 📁 File Ownership (Avoid Conflicts)

### To minimize conflicts, assign areas:

**Backend/app/ml/**
- Member 2 (ML Models)

**Backend/app/routes/**
- Member 3 (Backend API)

**Frontend/src/pages/**
- Member 4 (Frontend UI)

**Frontend/src/components/**
- Member 4 (Frontend UI)

**Documentation/**
- Member 5 (Testing & Docs)

**If you need to edit someone else's area:**
- Communicate first!
- Create a branch
- Tag them in the PR

---

## 🛠️ Common Commands Reference

### Get Latest Code
```bash
git checkout main
git pull origin main
```

### Create New Branch
```bash
git checkout -b feature/my-feature
```

### Check Status
```bash
git status
git branch  # See all branches
```

### Switch Branches
```bash
git checkout main
git checkout feature/other-branch
```

### Update Your Branch with Main
```bash
git checkout feature/my-branch
git merge main
```

### Delete Local Branch
```bash
git branch -d feature/old-branch
```

### See Commit History
```bash
git log --oneline
```

---

## 📞 Communication Rules

### Use GitHub Issues for:
- Bug reports
- Feature requests
- Task assignments

### Use Pull Request Comments for:
- Code review feedback
- Technical discussions
- Implementation questions

### Use WhatsApp/Discord for:
- Quick questions
- Coordination
- "I'm working on X file"

---

## 🎯 Best Practices

### DO:
- ✅ Pull main before creating new branch
- ✅ Create small, focused branches
- ✅ Write clear commit messages
- ✅ Test your changes locally
- ✅ Review others' PRs
- ✅ Communicate what you're working on

### DON'T:
- ❌ Push directly to main
- ❌ Work on main branch
- ❌ Create huge PRs (split into smaller ones)
- ❌ Commit broken code
- ❌ Ignore merge conflicts
- ❌ Edit same files simultaneously without communication

---

## 🚨 Emergency: Broke Something?

### If you pushed bad code:

```bash
# Revert last commit
git revert HEAD
git push origin main
```

### If main is broken:

1. Create hotfix branch
2. Fix the issue
3. Create PR with "HOTFIX" in title
4. Merge immediately after quick review

---

## 📊 Example Workflow

### Member 2 wants to add Liver Model:

```bash
# Day 1
git checkout main
git pull origin main
git checkout -b model/liver-function

# Add files: Backend/app/ml/liver_predictor.py
# Add files: Backend/ml_train/train_liver_model.py

git add .
git commit -m "Add: Liver function ML model with XGBoost"
git push origin model/liver-function

# Create PR on GitHub
# Tag Member 1 and Member 3 for review
```

### Member 1 reviews and merges:

```bash
# On GitHub: Review code, approve, merge
```

### Everyone else updates:

```bash
git checkout main
git pull origin main
# Now everyone has the liver model!
```

---

## 🎓 Learning Resources

- **Git Basics**: https://git-scm.com/book/en/v2
- **GitHub Flow**: https://guides.github.com/introduction/flow/
- **Pull Requests**: https://docs.github.com/en/pull-requests

---

## 📝 Quick Checklist

Before starting work:
- [ ] `git checkout main`
- [ ] `git pull origin main`
- [ ] `git checkout -b feature/my-feature`

Before creating PR:
- [ ] Tested locally
- [ ] Clear commit messages
- [ ] No conflicts with main
- [ ] Descriptive PR title and description

After PR merged:
- [ ] `git checkout main`
- [ ] `git pull origin main`
- [ ] Delete old branch

---

## 🎉 Benefits of This Workflow

- ✅ No one breaks production
- ✅ Code review catches bugs
- ✅ Clear history of who did what
- ✅ Easy to revert if needed
- ✅ Professional workflow experience
- ✅ Parallel work without conflicts

---

## 🆘 Need Help?

**Git Issues:**
- Check this guide first
- Ask in team chat
- Google the error message

**Merge Conflicts:**
- Ask the person who wrote the conflicting code
- Discuss the best way to merge

**Stuck:**
- Don't force push!
- Ask team lead (Member 1)
- Share your screen if needed

---

**Remember: Communication is key! Always let the team know what you're working on.**

**Happy Collaborating! 🚀**
