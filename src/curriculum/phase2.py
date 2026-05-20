# Phase 2: Developer Tools — Git and Maven
TOPICS = [
  {
    "id": 23,
    "phase": "Developer Tools",
    "phaseColor": "tools",
    "phaseClass": "ph-tools",
    "title": "Git Fundamentals: Version Control That Saved Software Engineering",
    "hours": 5,
    "complexity": "beginner",
    "importance": "critical",
    "textbook": "Chacon & Straub, Pro Git (2nd ed), Chapters 1-3",
    "summary": "Repositories, commits, staging area, branches, merging, remotes, and the Git mental model that every developer must internalize.",
    "lesson": "<h4>Introduction: Why Git Won and What Problem It Solves</h4><p>Before Git (released 2005 by Linus Torvalds), version control was centralized (SVN, CVS). Every commit required a network connection. Branches were expensive copies. Merging was painful. Linux kernel development — thousands of contributors across the globe — needed something fundamentally different. Git solved this with a <strong>distributed model</strong>: every developer has a complete copy of the entire repository history on their local machine. Commits are instant. Branches are lightweight pointers. Merging is a first-class operation.</p><p>Today, Git is used by over 90% of professional developers (Stack Overflow Survey 2024). It is not optional — it is the air you breathe as a software engineer. Understanding Git deeply means never losing work, confidently experimenting in branches, and collaborating without fear of conflicts.</p><h4>The Git Mental Model: Snapshots, Not Diffs</h4><p>Most VCS systems (SVN, CVS) store <strong>deltas</strong> — the differences between versions. Git stores <strong>snapshots</strong> — a complete copy of every file at each commit. Files that haven't changed are stored as pointers to the previous identical version. This seems wasteful but is actually brilliant: (1) switching between versions is instant (no delta computation), (2) every clone is a full backup, (3) operations like diff and blame are optimized because Git knows the complete state at every point.</p><p>Git has three areas, and understanding them is the key to mastering Git:</p><ol><li><strong>Working Directory:</strong> Your actual files on disk. This is what you edit.</li><li><strong>Staging Area (Index):</strong> A middle ground where you build the next commit. <code>git add</code> moves changes here. This lets you craft precise, meaningful commits instead of dumping all changes at once.</li><li><strong>Repository (.git/):</strong> The commit history. <code>git commit</code> takes the staging area and creates an immutable snapshot with a SHA-1 hash, author, timestamp, and message.</li></ol><div class='key-point'><strong>Mental model:</strong> Working Directory → (git add) → Staging Area → (git commit) → Repository. Each commit points to its parent(s), forming a directed acyclic graph (DAG). A branch is just a movable pointer to a commit. HEAD points to the current branch. This is the entire conceptual foundation of Git.</div><h4>Essential Git Commands — Your Daily Toolkit</h4><div class='code-block'><span class='lang-tag'>bash</span><pre><span class='cm'># Initialize a repository — creates .git/ directory</span>\ngit init\n\n<span class='cm'># Check status — your most-used Git command</span>\ngit status\n\n<span class='cm'># Stage specific files (not everything — be deliberate)</span>\ngit add src/Main.java\n\n<span class='cm'># Commit with a meaningful message</span>\ngit commit -m <span class='st'>\"Add user authentication service\"</span>\n\n<span class='cm'># View commit history</span>\ngit log --oneline --graph --all\n\n<span class='cm'># See what you changed (unstaged changes)</span>\ngit diff\n\n<span class='cm'># See what's staged for commit</span>\ngit diff --staged\n\n<span class='cm'># Remove a file (stages the deletion)</span>\ngit rm old-file.java\n\n<span class='cm'># Move/rename a file</span>\ngit mv old-name.java new-name.java</pre></div><h4>The .gitignore File — What NOT to Version Control</h4><p>Compiled bytecode (.class), build artifacts (dist/, target/), IDE settings (.idea/), OS files (.DS_Store), and credentials (.env) should NEVER be committed. The .gitignore file tells Git to ignore them. Patterns use glob syntax: <code>*.class</code> matches all class files, <code>dist/</code> matches the dist directory, <code>!important.class</code> negates a previous pattern.</p><div class='code-block'><span class='lang-tag'>gitignore</span><pre><span class='cm'># Build output</span>\ndist/\ntarget/\n*.class\n\n<span class='cm'># IDE</span>\n.idea/\n*.iml\n\n<span class='cm'># OS</span>\n.DS_Store\nThumbs.db\n\n<span class='cm'># Secrets</span>\n.env\n*.pem</pre></div><h4>Commit Messages — Your Future Self Will Thank You</h4><p>A Git commit message is documentation that never goes out of date. The industry standard (from the Git project itself and adopted by Google, Microsoft, and most open-source projects): (1) a <strong>subject line</strong> limited to 50 characters, capitalized, imperative mood (\"Add feature\" not \"Added feature\"), (2) a blank line, (3) a <strong>body</strong> wrapped at 72 characters explaining WHAT changed and WHY (the diff shows HOW). A well-crafted commit message answers: why is this change necessary? How does it address the issue? What side effects should reviewers consider?</p><div class='code-block'><span class='lang-tag'>text</span><pre>Add rate limiting to authentication endpoint\n\nBrute force attacks on /api/auth/login increased 300% this quarter.\nIntroduce token bucket algorithm with 5 requests/second per IP.\nFailed attempts return 429 with Retry-After header.\n\nResolves: SEC-421</pre></div><div class='key-point'><strong>The three Git areas are the foundation:</strong> Working Directory (your files) → Staging Area (git add) → Repository (git commit). A branch is a pointer to a commit. HEAD is where you are now. Git stores snapshots, not diffs. Every clone is a complete backup of the entire history.</div>",
    "quiz": [
      {
        "question": "What is the primary difference between Git and centralized VCS like SVN?",
        "options": ["Git is faster at committing", "Git is distributed — every developer has a complete local copy of the entire repository history", "Git uses a different diff algorithm", "Git only works on Linux"],
        "correct": 1,
        "explanation": "Git is distributed: every clone contains the FULL repository history. Commits, diffs, and logs work offline. SVN requires a network connection for most operations."
      },
      {
        "question": "What does 'git add' do?",
        "options": ["Commits changes to the repository", "Copies files from the repository to the working directory", "Stages changes from the working directory to the staging area (index)", "Deletes tracked files"],
        "correct": 2,
        "explanation": "git add moves changes from the working directory to the staging area. This is the middle step before git commit, allowing you to craft precise commits."
      },
      {
        "question": "What is a Git commit identified by?",
        "options": ["An incrementing integer", "A timestamp only", "A SHA-1 cryptographic hash of the commit contents", "The author's name and email"],
        "correct": 2,
        "explanation": "Each commit is identified by a 40-character SHA-1 hash computed from the commit's contents (files, message, author, timestamp, parent hashes). This ensures integrity — any change to history changes all subsequent hashes."
      },
      {
        "question": "What is the purpose of the .gitignore file?",
        "options": ["To list all tracked files", "To specify files and directories Git should intentionally ignore", "To configure Git user settings", "To store commit message templates"],
        "correct": 1,
        "explanation": ".gitignore tells Git which files to exclude from version control: build artifacts, IDE files, OS metadata, and credentials should never be committed."
      },
      {
        "question": "Which area does 'git commit' take changes from?",
        "options": ["Working directory directly", "The remote repository", "The staging area (index)", "The stash"],
        "correct": 2,
        "explanation": "git commit creates a snapshot from the staging area, NOT directly from the working directory. This is why you must git add first — the staging area lets you choose exactly what goes into each commit."
      },
      {
        "question": "What does 'git status' show?",
        "options": ["Remote repository URL", "Commit history", "Current state of working directory and staging area — modified, staged, untracked files", "The contents of .gitignore"],
        "correct": 2,
        "explanation": "git status shows which files are modified (unstaged), staged for commit, or untracked. It's the most frequently used Git command for understanding current state."
      },
      {
        "question": "What is the imperative mood in commit messages and why is it used?",
        "options": ["A legal requirement", "Add feature' (not 'Added feature') — matches Git's own auto-generated messages and describes what the commit DOES", "It's shorter than past tense", "It's a Git technical limitation"],
        "correct": 1,
        "explanation": "Git itself generates messages in imperative mood (\"Merge branch\", \"Revert commit\"). Consistency with Git's own convention is the standard adopted by Linux, Google, and most open-source projects."
      },
      {
        "question": "What is a Git repository physically?",
        "options": ["A cloud service", "A .git directory containing the complete object database and references", "A database on a remote server", "Just the working directory files"],
        "correct": 1,
        "explanation": "The .git/ directory contains the entire repository: all commits (objects), branches and tags (refs), staging area (index), and configuration. Everything Git needs is in this one directory."
      },
      {
        "question": "What information is NOT stored in a Git commit?",
        "options": ["Author name and email", "Commit message", "The complete file contents at that point (snapshot)", "The exact time of day the commit was made to the second"],
        "correct": 3,
        "explanation": "Git stores: tree (file structure), parent commit hash(es), author, committer, message, and timestamp with timezone. The file contents are stored as blob objects referenced by the tree."
      },
      {
        "question": "What happens when you run 'git init'?",
        "options": ["It downloads the latest code from GitHub", "It creates a .git directory with the initial repository structure", "It copies all files to a backup location", "It opens the Git GUI"],
        "correct": 1,
        "explanation": "git init creates the .git/ directory containing: objects/ (where all content is stored), refs/ (branches and tags), HEAD (current branch pointer), and config (repository settings). No files are tracked until you git add and git commit."
      }
    ],
    "codingExercise": {
      "instruction": "Create a new directory, initialize a Git repository, create two Java files, commit them separately with meaningful messages, then view the commit history. Demonstrate: (1) git init, (2) git add with specific files (not git add .), (3) git commit with proper imperative messages, (4) git log --oneline to verify history.",
      "hint": "mkdir git-practice && cd git-practice && git init. Create Hello.java and Calculator.java. Add and commit Hello.java first, then Calculator.java. Use git log --oneline to see both commits.",
      "checkKeywords": ["git init", "git add", "git commit", "git log", "git status"]
    }
  },
  {
    "id": 24,
    "phase": "Developer Tools",
    "phaseColor": "tools",
    "phaseClass": "ph-tools",
    "title": "Git Branching, Merging & Collaboration",
    "hours": 6,
    "complexity": "intermediate",
    "importance": "critical",
    "textbook": "Chacon & Straub, Pro Git (2nd ed), Chapters 3, 5-6",
    "summary": "Branching strategies, merge vs rebase, resolving conflicts, pull requests, remote workflows, and the GitHub/GitLab collaboration model.",
    "lesson": "<h4>Introduction: Branches Are Why Git Changed Everything</h4><p>In centralized VCS systems (SVN, CVS), creating a branch meant copying the entire codebase — a slow, expensive operation. In Git, a branch is just a <strong>40-byte file containing the SHA-1 hash of the commit it points to</strong>. Creating a branch is instantaneous and costs essentially nothing. This fundamentally changed how developers work: you can create a branch for every feature, every bug fix, every experiment. When it works, merge it. When it doesn't, delete it. No cost, no risk, no coordination needed.</p><p>This lightweight branching model is the foundation of modern software development workflows: GitHub Flow, GitLab Flow, and Git Flow all depend on Git's ability to create and merge branches efficiently. A team of 100 developers might have 300 active branches at any given time — something impossible in pre-Git version control.</p><h4>Branches, HEAD, and the Commit Graph</h4><p>Internally, Git is a directed acyclic graph (DAG) of commits. Each commit points to its parent(s). A <strong>branch</strong> is a named pointer to a specific commit. <strong>HEAD</strong> is a special pointer indicating where you currently are — usually pointing to a branch name. When you make a new commit, the current branch pointer moves forward to the new commit, and HEAD follows (since it points to the branch).</p><p>This pointer model explains all Git branch behavior: creating a branch just writes a 40-byte file. Switching branches just changes where HEAD points and updates the working directory. Merging creates a new commit with two parents. Deleting a branch just removes the pointer file — the commits remain (protected by the reflog for 30-90 days).</p><div class='code-block'><span class='lang-tag'>bash</span><pre><span class='cm'># Create a new branch (lightweight pointer — instant)</span>\ngit branch feature-login\n\n<span class='cm'># Switch to that branch</span>\ngit switch feature-login\n\n<span class='cm'># Create AND switch in one command (most common)</span>\ngit switch -c feature-login\n\n<span class='cm'># List all branches (* marks current)</span>\ngit branch\n\n<span class='cm'># Delete a merged branch (safe — won't delete unmerged work)</span>\ngit branch -d feature-login\n\n<span class='cm'># Force delete (dangerous — discards unmerged work)</span>\ngit branch -D experiment</pre></div><h4>Merging: The Two Strategies</h4><p>Git has two fundamentally different ways to integrate changes from one branch into another:</p><p><strong>1. Merge (git merge):</strong> Creates a new \"merge commit\" with two parents — the tips of both branches. This preserves complete history and is the default for integrating feature branches into main. The merge commit is explicit: \"at this point, these two lines of development were combined.\" This is the standard for public branches and team collaboration.</p><p><strong>2. Rebase (git rebase):</strong> Replays the commits from your branch onto the tip of another branch, one by one, creating new commits with new hashes. The result is a linear, clean history — as if you had done all your work sequentially after the latest main. This is preferred for keeping feature branches up-to-date before merging. <strong>Golden rule: never rebase commits that have been pushed to a shared repository.</strong> Rebasing rewrites commit hashes, which destroys the shared history that other team members depend on.</p><div class='key-point'><strong>Decision framework:</strong> Use merge for integrating completed features into shared branches (preserves context). Use rebase for keeping your local feature branch up-to-date with main (clean history). Never rebase pushed commits. When in doubt, merge — it's always safe.</div><h4>Merge Conflicts: When Git Needs Your Judgment</h4><p>Git automatically merges changes that don't overlap. But when two branches modify the <strong>same lines</strong> of the same file, Git cannot determine which version is correct — this is a merge conflict. Git marks the conflicted file with both versions:</p><div class='code-block'><span class='lang-tag'>text</span><pre><span class='kw'><<<<<<<</span> HEAD (your current branch)\n<span class='kw'>public void</span> <span class='mt'>processOrder</span>(<span class='tp'>Order</span> order) {\n    validateInventory(order);\n<span class='kw'>=======</span>\n<span class='kw'>public void</span> <span class='mt'>processOrder</span>(<span class='tp'>Order</span> order) {\n    validatePayment(order);\n<span class='kw'>>>>>>></span> feature/new-validation</pre></div><p>Resolution steps: (1) Edit the file to keep the correct version (or a combination of both), (2) Remove the conflict markers (<<<, ===, >>>), (3) git add the resolved file, (4) git commit to complete the merge. Modern IDEs (IntelliJ, VS Code) provide visual three-way merge tools that make this process far easier than manual editing.</p><h4>Remote Collaboration: GitHub Flow</h4><p>GitHub Flow (used by GitHub, and adopted by thousands of teams) is the simplest effective branching model:</p><ol><li><strong>main branch is always deployable.</strong> Never commit directly to main.</li><li><strong>Create a descriptive branch</strong> from main: <code>feature/add-2fa</code>, <code>fix/login-timeout</code>, <code>docs/api-guide</code>.</li><li><strong>Commit and push</strong> to your branch regularly — \"commit early, commit often.\"</li><li><strong>Open a Pull Request</strong> when you want feedback or are ready to merge. PRs are where code review happens.</li><li><strong>Discuss, review, and iterate</strong> with your team using the PR as the collaboration hub.</li><li><strong>Merge to main</strong> once approved, then deploy. Delete the feature branch.</li></ol><div class='code-block'><span class='lang-tag'>bash</span><pre><span class='cm'># Clone a repository (downloads complete history)</span>\ngit clone git@github.com:team/project.git\n\n<span class='cm'># Create feature branch and switch to it</span>\ngit switch -c feature/add-2fa\n\n<span class='cm'># Work, commit, push regularly</span>\ngit add src/auth/TwoFactorAuth.java\ngit commit -m <span class='st'>\"Add TOTP-based two-factor authentication\"</span>\ngit push -u origin feature/add-2fa\n\n<span class='cm'># Keep branch up-to-date with main (rebase preferred for local)</span>\ngit switch main\ngit pull origin main\ngit switch feature/add-2fa\ngit rebase main\n\n<span class='cm'># After PR approval and merge, clean up</span>\ngit switch main\ngit pull origin main\ngit branch -d feature/add-2fa</pre></div><div class='key-point'><strong>Branching summary:</strong> A branch is a 40-byte pointer to a commit. Creating/deleting branches is free. Merge preserves history with a merge commit. Rebase creates linear history but rewrites hashes — never rebase pushed commits. GitHub Flow: branch → commit → PR → review → merge → delete branch.</div>",
    "quiz": [
      {
        "question": "What is a Git branch internally?",
        "options": ["A complete copy of the codebase", "A 40-byte file containing the SHA-1 hash of the commit it points to", "A separate directory with all files", "A diff from the main branch"],
        "correct": 1,
        "explanation": "A branch is just a lightweight movable pointer to a commit — a 40-byte file in .git/refs/heads/ containing a SHA-1 hash. This is why branches are instant and free to create."
      },
      {
        "question": "What is the fundamental difference between git merge and git rebase?",
        "options": ["No difference — they achieve the same result", "Merge creates a merge commit preserving history; rebase replays commits creating new hashes for linear history", "Rebase is always safer", "Merge cannot handle conflicts"],
        "correct": 1,
        "explanation": "Merge creates a new commit with two parents, preserving complete history. Rebase replays commits onto the target branch tip, creating new commits with new hashes — producing linear history but rewriting commit history."
      },
      {
        "question": "What is the golden rule of rebasing?",
        "options": ["Always rebase before pushing", "Never rebase commits that have been pushed to a shared repository", "Rebase only on Fridays", "Always use rebase instead of merge"],
        "correct": 1,
        "explanation": "Rebasing rewrites commit hashes. If those commits have been pushed and others have based work on them, rebasing destroys the shared history and causes chaos. Rebase only local, unpushed commits."
      },
      {
        "question": "What markers does Git use to indicate merge conflicts?",
        "options": ["// CONFLICT START and // CONFLICT END", "<<<<<<<, =======, and >>>>>>>", "/* MERGE ERROR */", "!CONFLICT!"],
        "correct": 1,
        "explanation": "Git marks conflicts with <<<<<<< (current branch), ======= (separator), and >>>>>>> (incoming branch). Edit the file to resolve, remove markers, git add, git commit."
      },
      {
        "question": "What is GitHub Flow's core principle?",
        "options": ["Commit directly to main for speed", "The main branch is always deployable — all work happens in feature branches with pull requests", "Use rebase exclusively", "Never delete branches after merging"],
        "correct": 1,
        "explanation": "GitHub Flow: main is always production-ready. Work happens in descriptive feature branches. Pull requests enable code review. After merge, delete the branch."
      },
      {
        "question": "What does 'git pull' actually do?",
        "options": ["Downloads changes without merging", "git fetch followed by git merge (or git rebase if configured)", "Only updates remote tracking branches", "Deletes local changes and replaces with remote"],
        "correct": 1,
        "explanation": "git pull = git fetch (download remote changes) + git merge (integrate them). With --rebase flag, it becomes fetch + rebase instead. Some prefer fetch first to inspect changes before merging."
      },
      {
        "question": "What is 'detached HEAD' state?",
        "options": ["A Git error that corrupts the repository", "When HEAD points directly to a commit (not a branch) — any new commits will be orphaned unless you create a branch", "When the repository is disconnected from the remote", "A deprecated Git feature"],
        "correct": 1,
        "explanation": "Detached HEAD means HEAD points to a specific commit SHA instead of a branch name. New commits in this state are not on any branch and will be garbage-collected unless you create a branch pointing to them."
      },
      {
        "question": "What does 'git stash' do?",
        "options": ["Permanently deletes uncommitted changes", "Temporarily saves uncommitted changes and restores a clean working directory", "Commits changes to a special branch", "Reverts to the last commit"],
        "correct": 1,
        "explanation": "git stash shelves modified tracked files and staged changes, reverting the working directory to match HEAD. git stash pop reapplies the stashed changes. Useful when you need to switch branches with uncommitted work."
      },
      {
        "question": "What is a fast-forward merge?",
        "options": ["A merge that skips conflict resolution", "When the target branch has no new commits since the source branch diverged — Git simply moves the branch pointer forward", "A merge using rebase internally", "A deprecated merge strategy"],
        "correct": 1,
        "explanation": "If main has no new commits since feature branched off, merging feature into main just moves the main pointer forward to feature's tip. No merge commit needed. Use git merge --no-ff to force a merge commit for documentation."
      },
      {
        "question": "What is the purpose of a Pull Request (PR)?",
        "options": ["To download code from the remote", "To propose changes, enable code review, run CI checks, and discuss before merging into a protected branch", "To automatically fix merge conflicts", "To backup the repository"],
        "correct": 1,
        "explanation": "A PR is a request to merge one branch into another. It's the collaboration hub: reviewers see the diff, CI runs tests, team discusses, and the merge happens only after approval. PR = code review + discussion + CI gating."
      }
    ],
    "codingExercise": {
      "instruction": "Simulate a feature branch workflow: (1) Create a main branch with an initial commit, (2) Create a feature branch, (3) Make commits on both branches creating a merge conflict, (4) Resolve the conflict manually, (5) Complete the merge. Write the sequence of commands and explain each step in comments.",
      "hint": "Use git switch -c to create branches. Create a file on main with some content, then modify the same lines differently on the feature branch. git merge will report the conflict. Edit the file, remove markers, git add, git commit.",
      "checkKeywords": ["git switch", "git merge", "conflict", "git add", "git commit", "<<<<<<<"]
    }
  },
  {
    "id": 25,
    "phase": "Developer Tools",
    "phaseColor": "tools",
    "phaseClass": "ph-tools",
    "title": "Maven Fundamentals: Build Automation That Standardized Java",
    "hours": 5,
    "complexity": "beginner",
    "importance": "critical",
    "textbook": "Maven: The Definitive Guide (Sonatype), Chapters 1-5",
    "summary": "POM structure, coordinates (groupId/artifactId/version), dependency management, the local repository (~/.m2), plugins, and the Maven lifecycle.",
    "lesson": "<h4>Introduction: Why Maven Exists and What Problem It Solved</h4><p>Before Maven (released 2004 by Jason van Zyl at Sonatype), Java projects were built with Ant (2000). Ant was an improvement over manual shell scripts but had a fundamental flaw: it was <strong>imperative</strong> — you told Ant exactly what to do (compile these files, copy here, jar there). Every project had a different build script. Dependencies were managed manually — you downloaded JARs and put them in a lib/ folder, committing them to version control. There was no standard project structure, no dependency resolution, and no build lifecycle.</p><p>Maven introduced <strong>declarative builds</strong>: you describe WHAT your project is (a JAR, a WAR, a Spring Boot app) and WHAT it depends on. Maven handles HOW to build it through a standardized lifecycle. This \"convention over configuration\" philosophy means: (1) every Maven project has the same directory structure, (2) dependencies are declared once and downloaded automatically from Maven Central, (3) the build lifecycle (compile → test → package → install) is standardized across all projects. Any developer can navigate any Maven project because the structure is always the same.</p><h4>The POM: Project Object Model</h4><p>The <code>pom.xml</code> file is the single source of truth for a Maven project. It declares: (1) <strong>project coordinates</strong> (groupId, artifactId, version) — the unique identifier for your artifact, (2) <strong>dependencies</strong> — libraries your project needs, (3) <strong>plugins</strong> — build tools that extend the lifecycle, (4) <strong>properties</strong> — configuration values. The POM is XML, and while verbose, its structure is rigid and predictable — IDEs and tools can reliably parse and manipulate it.</p><div class='code-block'><span class='lang-tag'>xml</span><pre><span class='kw'>&lt;?xml version=\"1.0\"?&gt;</span>\n<span class='kw'>&lt;project&gt;</span>\n    <span class='cm'>&lt;!-- Coordinates: uniquely identify this artifact --&gt;</span>\n    <span class='kw'>&lt;groupId&gt;</span>com.example<span class='kw'>&lt;/groupId&gt;</span>\n    <span class='kw'>&lt;artifactId&gt;</span>order-service<span class='kw'>&lt;/artifactId&gt;</span>\n    <span class='kw'>&lt;version&gt;</span>1.0.0<span class='kw'>&lt;/version&gt;</span>\n    <span class='kw'>&lt;packaging&gt;</span>jar<span class='kw'>&lt;/packaging&gt;</span>\n\n    <span class='cm'>&lt;!-- Properties for version management --&gt;</span>\n    <span class='kw'>&lt;properties&gt;</span>\n        <span class='kw'>&lt;java.version&gt;</span>21<span class='kw'>&lt;/java.version&gt;</span>\n    <span class='kw'>&lt;/properties&gt;</span>\n\n    <span class='cm'>&lt;!-- Dependencies: libraries from Maven Central --&gt;</span>\n    <span class='kw'>&lt;dependencies&gt;</span>\n        <span class='kw'>&lt;dependency&gt;</span>\n            <span class='kw'>&lt;groupId&gt;</span>org.springframework.boot<span class='kw'>&lt;/groupId&gt;</span>\n            <span class='kw'>&lt;artifactId&gt;</span>spring-boot-starter-web<span class='kw'>&lt;/artifactId&gt;</span>\n            <span class='kw'>&lt;version&gt;</span>3.3.0<span class='kw'>&lt;/version&gt;</span>\n        <span class='kw'>&lt;/dependency&gt;</span>\n    <span class='kw'>&lt;/dependencies&gt;</span>\n<span class='kw'>&lt;/project&gt;</span></pre></div><h4>Maven Coordinates: The Universal Address System</h4><p>Every artifact in the Maven ecosystem is uniquely identified by three coordinates, plus a packaging type:</p><ul><li><strong>groupId:</strong> Reverse domain name (com.example, org.apache). Groups related projects together. Think of it as the organization or project namespace.</li><li><strong>artifactId:</strong> The project name within the group (order-service, commons-lang). Must be unique within the groupId.</li><li><strong>version:</strong> The specific release. SNAPSHOT versions (1.0-SNAPSHOT) are mutable development versions; release versions (1.0.0) are immutable. Maven checks for SNAPSHOT updates periodically.</li><li><strong>packaging:</strong> The output format: jar (default), war (web application), pom (parent POM).</li></ul><p>These coordinates are the universal naming convention for the entire Java ecosystem. When you declare a dependency, Maven resolves these coordinates against repositories (Maven Central by default) and downloads the artifact plus its transitive dependencies automatically.</p><h4>Dependency Management: Transitive Dependencies and Scope</h4><p>One of Maven's most powerful features is <strong>transitive dependency resolution</strong>. If your project depends on Library A, and Library A depends on Libraries B and C, Maven automatically downloads B and C — you don't need to declare them. Maven builds a dependency tree and resolves version conflicts using a \"nearest definition\" rule: the version closest to your project in the dependency tree wins.</p><p>Dependency <strong>scope</strong> controls when a dependency is available: <code>compile</code> (default, available everywhere), <code>test</code> (only for test compilation/execution — JUnit, Mockito), <code>runtime</code> (not needed for compilation but required at runtime — JDBC drivers), <code>provided</code> (provided by the runtime environment — Servlet API in a Java EE container).</p><div class='key-point'><strong>Maven dependency philosophy:</strong> Declare direct dependencies only — transitive dependencies come automatically. Never commit JAR files to version control. Use dependency scope to control availability. Run mvn dependency:tree to visualize the complete dependency graph.</div><h4>The Maven Build Lifecycle: Phases, Not Steps</h4><p>Maven defines a standard build lifecycle consisting of <strong>phases</strong> (not steps). When you run a phase, all preceding phases execute automatically. The default lifecycle:</p><ol><li><strong>validate:</strong> Check project structure and configuration.</li><li><strong>compile:</strong> Compile source code (javac).</li><li><strong>test:</strong> Run unit tests (JUnit, TestNG). Tests must pass for the build to continue.</li><li><strong>package:</strong> Create the distributable (JAR, WAR).</li><li><strong>verify:</strong> Run integration tests and quality checks.</li><li><strong>install:</strong> Install the artifact into the local repository (~/.m2).</li><li><strong>deploy:</strong> Upload the artifact to a remote repository for sharing.</li></ol><p>When you run <code>mvn install</code>, Maven executes validate → compile → test → package → verify → install in sequence. Each phase delegates to <strong>plugin goals</strong>: the compile phase runs <code>maven-compiler-plugin:compile</code>, the test phase runs <code>maven-surefire-plugin:test</code>, and so on. This separation of lifecycle phases from plugin implementations is what makes Maven extensible.</p><div class='code-block'><span class='lang-tag'>bash</span><pre><span class='cm'># Compile only (no tests)</span>\nmvn compile\n\n<span class='cm'># Run tests (compiles first automatically)</span>\nmvn test\n\n<span class='cm'># Create JAR (all preceding phases execute)</span>\nmvn package\n\n<span class='cm'># Install to local repo (~/.m2)</span>\nmvn install\n\n<span class='cm'># Clean build output before building</span>\nmvn clean package\n\n<span class='cm'># Skip tests (use sparingly — only for quick dev iteration)</span>\nmvn package -DskipTests</pre></div><h4>The Local Repository: ~/.m2</h4><p>Maven caches all downloaded artifacts in <code>~/.m2/repository/</code> (on macOS/Linux) or <code>%USERPROFILE%\\.m2\\repository\\</code> (on Windows). This local repository serves two purposes: (1) <strong>cache:</strong> once downloaded, artifacts are reused across all projects, (2) <strong>install target:</strong> <code>mvn install</code> puts your project's artifact here so other local projects can depend on it. The remote repository (Maven Central by default) is checked only when an artifact is not found locally.</p><div class='key-point'><strong>Maven philosophy:</strong> Convention over configuration. Standard directory layout (src/main/java, src/test/java). Declarative POM (WHAT, not HOW). Transitive dependency management. Standardized build lifecycle. These conventions mean any developer can work on any Maven project without documentation.</div>",
    "quiz": [
      {
        "question": "What problem did Maven solve that Ant could not?",
        "options": ["Faster compilation", "Declarative builds with standardized lifecycle, automatic dependency management, and convention over configuration", "Better IDE integration", "Support for multiple programming languages"],
        "correct": 1,
        "explanation": "Ant was imperative (HOW to build). Maven is declarative (WHAT to build). Maven introduced standardized lifecycle phases, automatic dependency resolution from Maven Central, and convention over configuration."
      },
      {
        "question": "What three coordinates uniquely identify a Maven artifact?",
        "options": ["name, version, author", "groupId, artifactId, version", "package, class, method", "namespace, module, revision"],
        "correct": 1,
        "explanation": "groupId (organization namespace), artifactId (project name), and version (specific release) together uniquely identify any artifact in the Maven ecosystem."
      },
      {
        "question": "What does 'mvn install' do?",
        "options": ["Downloads and installs the JDK", "Executes all lifecycle phases up to install — compiles, tests, packages, then copies the artifact to the local repository (~/.m2)", "Installs Maven itself", "Uploads to Maven Central"],
        "correct": 1,
        "explanation": "mvn install runs validate → compile → test → package → verify → install. The install phase copies the built artifact to ~/.m2/repository where other local projects can use it."
      },
      {
        "question": "What is a SNAPSHOT version in Maven?",
        "options": ["A production release", "A mutable development version — Maven checks for updates periodically", "A broken build", "A version without dependencies"],
        "correct": 1,
        "explanation": "SNAPSHOT versions (e.g., 1.0-SNAPSHOT) represent development builds that can change. Maven re-downloads SNAPSHOTs periodically (or with -U flag). Release versions are immutable."
      },
      {
        "question": "Where does Maven store downloaded dependencies locally?",
        "options": ["In the project's lib/ folder", "In ~/.m2/repository/ (the local Maven repository)", "In /usr/local/maven/", "Dependencies are not stored locally"],
        "correct": 1,
        "explanation": "The local repository at ~/.m2/repository/ caches all downloaded artifacts. Once downloaded, they're available to all Maven projects without re-downloading. mvn install adds your project's artifacts here."
      },
      {
        "question": "What is transitive dependency resolution?",
        "options": ["Manually downloading all dependencies", "Maven automatically downloads dependencies of your dependencies — you only declare direct dependencies", "A deprecated Maven feature", "Converting JARs to source code"],
        "correct": 1,
        "explanation": "If A depends on B, and B depends on C and D, Maven automatically downloads C and D. You only need to declare A as a dependency. Run mvn dependency:tree to see the complete graph."
      },
      {
        "question": "What does 'mvn clean' do?",
        "options": ["Deletes source code", "Removes the target/ directory — all compiled output and build artifacts", "Clears the local repository cache", "Formats the POM file"],
        "correct": 1,
        "explanation": "mvn clean deletes the target/ directory, forcing a fresh recompilation on the next build. Often combined: mvn clean package ensures no stale artifacts remain."
      },
      {
        "question": "What is the standard Maven directory layout?",
        "options": ["Any structure works", "src/main/java (source), src/test/java (tests), src/main/resources (config files), target/ (build output), pom.xml (configuration)", "Only one directory for everything", "Maven doesn't enforce directory structure"],
        "correct": 1,
        "explanation": "Maven's convention: src/main/java for production code, src/test/java for tests, src/main/resources for non-code files, target/ for build output. This standardization means any developer can navigate any Maven project."
      },
      {
        "question": "What is the Maven Central Repository?",
        "options": ["A company-internal server", "The default public repository hosting millions of Java artifacts — Maven checks here first for dependencies", "A local file on your machine", "A deprecated service"],
        "correct": 1,
        "explanation": "Maven Central (repo.maven.apache.org) is the largest public repository of Java libraries, hosting millions of artifacts. Build tools download dependencies from here automatically."
      },
      {
        "question": "What is a Maven plugin?",
        "options": ["A browser extension", "A tool that extends the build lifecycle — each lifecycle phase delegates to plugin goals (compiler:compile, surefire:test, jar:jar)", "A dependency type", "A type of POM file"],
        "correct": 1,
        "explanation": "Maven itself is a plugin execution framework. The compile phase runs maven-compiler-plugin, test phase runs maven-surefire-plugin, package phase runs maven-jar-plugin. Plugins make Maven extensible."
      }
    ],
    "codingExercise": {
      "instruction": "Create a Maven project (manually or using mvn archetype:generate) with: (1) Standard directory layout, (2) A pom.xml with at least two dependencies (e.g., JUnit 5 for testing, Gson for JSON), (3) A simple Java class in src/main/java, (4) A unit test in src/test/java. Run mvn test and mvn package. Verify the JAR was created in target/.",
      "hint": "mvn archetype:generate -DgroupId=com.example -DartifactId=my-app creates the standard layout. Add dependencies to pom.xml. Run mvn test to compile and test. Run mvn package to create the JAR.",
      "checkKeywords": ["pom.xml", "dependency", "groupId", "mvn test", "mvn package", "src/main/java"]
    }
  },
  {
    "id": 26,
    "phase": "Developer Tools",
    "phaseColor": "tools",
    "phaseClass": "ph-tools",
    "title": "Maven Build Lifecycle, Plugins & Multi-Module Projects",
    "hours": 6,
    "complexity": "intermediate",
    "importance": "important",
    "textbook": "Maven: The Definitive Guide (Sonatype), Chapters 6-9",
    "summary": "Build lifecycle phases in depth, plugin configuration, multi-module projects, dependency management with BOM, profiles, and CI/CD integration.",
    "lesson": "<h4>Introduction: From Single Module to Enterprise Build</h4><p>A single-module Maven project is straightforward — one pom.xml, one source tree, one artifact. But real enterprise applications consist of dozens or hundreds of modules: an API module, a service module, a data access module, a web module, a shared utilities module. Each module has its own pom.xml, its own source tree, and produces its own artifact. Managing dependencies, versions, and build order across all these modules manually would be chaos. Maven solves this with a <strong>multi-module project</strong> (also called a reactor build) and <strong>dependency management</strong> through a parent POM or BOM (Bill of Materials).</p><h4>The Build Lifecycle in Depth</h4><p>Maven has three built-in lifecycles: <strong>default</strong> (build and deploy), <strong>clean</strong> (remove build output), and <strong>site</strong> (generate documentation). Each lifecycle consists of phases executed in order. Each phase is implemented by <strong>plugin goals</strong> bound to that phase. This separation of lifecycle (when) from plugins (how) is Maven's most elegant design decision:</p><div class='code-block'><span class='lang-tag'>text</span><pre>Phase              Plugin:Goal                         What Happens\n──────────────────────────────────────────────────────────────────\nvalidate                                               Check project is valid\ncompile            compiler:compile                    Compile source code\ntest               surefire:test                      Run unit tests\npackage            jar:jar / war:war                  Create distributable\nverify             failsafe:integration-test          Run integration tests\ninstall            install:install                    Copy to local ~/.m2\ndeploy             deploy:deploy                      Upload to remote repo</pre></div><p>When you run <code>mvn verify</code>, Maven executes all phases up to and including verify. You can bind additional plugin goals to any phase — for example, code quality checks (Checkstyle, SpotBugs) to the verify phase, or Docker image building to the package phase.</p><h4>Plugin Configuration: Extending the Build</h4><p>Plugins are configured in the POM's <code>&lt;build&gt;</code> section. Each plugin can have: (1) <strong>executions</strong> — binding goals to specific phases, (2) <strong>configuration</strong> — parameters for the plugin, (3) <strong>dependencies</strong> — libraries the plugin itself needs.</p><div class='code-block'><span class='lang-tag'>xml</span><pre><span class='kw'>&lt;build&gt;</span>\n    <span class='kw'>&lt;plugins&gt;</span>\n        <span class='cm'>&lt;!-- Compiler: set Java version --&gt;</span>\n        <span class='kw'>&lt;plugin&gt;</span>\n            <span class='kw'>&lt;groupId&gt;</span>org.apache.maven.plugins<span class='kw'>&lt;/groupId&gt;</span>\n            <span class='kw'>&lt;artifactId&gt;</span>maven-compiler-plugin<span class='kw'>&lt;/artifactId&gt;</span>\n            <span class='kw'>&lt;configuration&gt;</span>\n                <span class='kw'>&lt;release&gt;</span>21<span class='kw'>&lt;/release&gt;</span>\n            <span class='kw'>&lt;/configuration&gt;</span>\n        <span class='kw'>&lt;/plugin&gt;</span>\n    <span class='kw'>&lt;/plugins&gt;</span>\n<span class='kw'>&lt;/build&gt;</span></pre></div><h4>Multi-Module Projects: The Reactor Build</h4><p>A multi-module project has a root POM with <code>&lt;packaging&gt;pom&lt;/packaging&gt;</code> that declares its child modules. Each child module has its own pom.xml and inherits from the parent. Maven's reactor determines the correct build order based on inter-module dependencies — if module B depends on module A, A is built first automatically.</p><div class='code-block'><span class='lang-tag'>xml</span><pre><span class='cm'>&lt;!-- Root pom.xml (packaging=pom) --&gt;</span>\n<span class='kw'>&lt;modules&gt;</span>\n    <span class='kw'>&lt;module&gt;</span>order-api<span class='kw'>&lt;/module&gt;</span>\n    <span class='kw'>&lt;module&gt;</span>order-service<span class='kw'>&lt;/module&gt;</span>\n    <span class='kw'>&lt;module&gt;</span>order-data<span class='kw'>&lt;/module&gt;</span>\n    <span class='kw'>&lt;module&gt;</span>order-web<span class='kw'>&lt;/module&gt;</span>\n<span class='kw'>&lt;/modules&gt;</span></pre></div><h4>Dependency Management: The BOM Pattern</h4><p>In multi-module projects, keeping dependency versions consistent across modules is critical. If module A uses Spring 6.1 and module B uses Spring 6.0, you get version conflicts and mysterious runtime errors. Maven's <code>&lt;dependencyManagement&gt;</code> section in the parent POM solves this: it declares dependency versions (and exclusions, scopes) without actually adding dependencies. Child modules then declare dependencies without specifying versions — they inherit from the parent. This is the same pattern used by Spring Boot's spring-boot-dependencies BOM and the AWS SDK BOM.</p><div class='code-block'><span class='lang-tag'>xml</span><pre><span class='cm'>&lt;!-- Parent POM: declare versions centrally --&gt;</span>\n<span class='kw'>&lt;dependencyManagement&gt;</span>\n    <span class='kw'>&lt;dependencies&gt;</span>\n        <span class='kw'>&lt;dependency&gt;</span>\n            <span class='kw'>&lt;groupId&gt;</span>org.springframework.boot<span class='kw'>&lt;/groupId&gt;</span>\n            <span class='kw'>&lt;artifactId&gt;</span>spring-boot-dependencies<span class='kw'>&lt;/artifactId&gt;</span>\n            <span class='kw'>&lt;version&gt;</span>3.3.0<span class='kw'>&lt;/version&gt;</span>\n            <span class='kw'>&lt;type&gt;</span>pom<span class='kw'>&lt;/type&gt;</span>\n            <span class='kw'>&lt;scope&gt;</span>import<span class='kw'>&lt;/scope&gt;</span>\n        <span class='kw'>&lt;/dependency&gt;</span>\n    <span class='kw'>&lt;/dependencies&gt;</span>\n<span class='kw'>&lt;/dependencyManagement&gt;</span>\n\n<span class='cm'>&lt;!-- Child POM: inherit version from parent --&gt;</span>\n<span class='kw'>&lt;dependencies&gt;</span>\n    <span class='kw'>&lt;dependency&gt;</span>\n        <span class='kw'>&lt;groupId&gt;</span>org.springframework.boot<span class='kw'>&lt;/groupId&gt;</span>\n        <span class='kw'>&lt;artifactId&gt;</span>spring-boot-starter-web<span class='kw'>&lt;/artifactId&gt;</span>\n        <span class='cm'>&lt;!-- No version needed — inherited from parent --&gt;</span>\n    <span class='kw'>&lt;/dependency&gt;</span>\n<span class='kw'>&lt;/dependencies&gt;</span></pre></div><h4>Maven Profiles: Environment-Specific Builds</h4><p>Different environments (dev, staging, production) often need different configurations — database URLs, API keys, logging levels. Maven <strong>profiles</strong> allow you to define environment-specific build configurations that activate based on conditions (OS, JDK version, environment variable, or explicit -P flag).</p><div class='key-point'><strong>Maven at enterprise scale:</strong> Multi-module reactor builds manage complex project hierarchies. Dependency management centralizes version control. BOMs (Bill of Materials) ensure version consistency. Profiles handle environment-specific configuration. The build lifecycle provides the framework; plugins provide the implementation.</div>",
    "quiz": [
      {
        "question": "What is a Maven multi-module project?",
        "options": ["Multiple unrelated projects in one folder", "A root POM (packaging=pom) with child modules — each with its own pom.xml — built as a reactor", "A project with multiple main classes", "A deprecated Maven feature"],
        "correct": 1,
        "explanation": "A multi-module project has a root POM declaring child modules. Maven's reactor determines build order from inter-module dependencies. Each module produces its own artifact."
      },
      {
        "question": "What does the Maven reactor do?",
        "options": ["Runs tests in parallel", "Determines the correct build order for multi-module projects based on inter-module dependencies", "Generates HTML documentation", "Compiles Java code to native binaries"],
        "correct": 1,
        "explanation": "The reactor analyzes module dependencies and builds them in correct order. If module B depends on module A, A is built first automatically."
      },
      {
        "question": "What is the purpose of <dependencyManagement> in a parent POM?",
        "options": ["To add dependencies to every child module", "To declare dependency versions centrally — child modules inherit versions without re-declaring them", "To exclude transitive dependencies", "To download dependencies faster"],
        "correct": 1,
        "explanation": "dependencyManagement centralizes version declarations. It does NOT add dependencies — child modules still need their own <dependencies> section, but can omit the <version> tag."
      },
      {
        "question": "What is a BOM (Bill of Materials) in Maven?",
        "options": ["A build output file", "A POM that centralizes dependency versions for a set of related artifacts — imported via scope=import in dependencyManagement", "A deprecated Maven concept", "A type of plugin"],
        "correct": 1,
        "explanation": "A BOM POM declares versions for a set of related dependencies. Projects import the BOM in their dependencyManagement section to inherit all versions at once. Spring Boot, AWS SDK, and Jackson all provide BOMs."
      },
      {
        "question": "What are Maven build profiles used for?",
        "options": ["Developer profiles on GitHub", "Environment-specific build configurations — activated by OS, JDK version, or explicit -P flag", "Performance profiling", "Code coverage reports"],
        "correct": 1,
        "explanation": "Maven profiles define environment-specific configurations (dev vs prod database URLs, API keys). Activate with mvn -Pproduction package or automatically based on OS/JDK."
      },
      {
        "question": "What is the difference between mvn package and mvn install?",
        "options": ["No difference", "package creates the artifact in target/. install additionally copies it to ~/.m2/repository/ for use by other local projects", "install only runs tests", "package skips compilation"],
        "correct": 1,
        "explanation": "mvn package stops after creating the JAR/WAR. mvn install continues to the install phase, copying the artifact to the local repository where other projects can depend on it."
      },
      {
        "question": "How does a child POM inherit from a parent POM?",
        "options": ["Through Java inheritance", "Via the <parent> element specifying the parent's groupId, artifactId, and version", "Automatically by naming convention", "Through the Maven settings.xml file"],
        "correct": 1,
        "explanation": "A child POM declares a <parent> section with the parent's groupId, artifactId, and version. The child inherits properties, dependency versions, plugin configs, and repository settings."
      },
      {
        "question": "What does 'mvn dependency:tree' show?",
        "options": ["File system structure", "The complete dependency hierarchy — which libraries your project depends on, including transitive dependencies and version conflicts", "Maven's internal file tree", "The project's directory structure"],
        "correct": 1,
        "explanation": "mvn dependency:tree prints the full dependency graph showing direct and transitive dependencies with their versions. Invaluable for debugging version conflicts and understanding what libraries are being pulled in."
      },
      {
        "question": "What is the Maven wrapper (mvnw)?",
        "options": ["A Docker container for Maven", "A script (mvnw/mvnw.cmd) checked into version control that downloads and uses a specific Maven version — no pre-installed Maven needed", "A deprecated Maven plugin", "A GUI for Maven"],
        "correct": 1,
        "explanation": "The Maven wrapper ensures every developer and CI pipeline uses the exact same Maven version. Run ./mvnw instead of mvn. The wrapper script downloads Maven automatically if not present."
      },
      {
        "question": "What is the purpose of the maven-enforcer-plugin?",
        "options": ["To speed up builds", "To enforce project rules: required Java version, banned dependencies, consistent plugin versions across modules", "To enforce code style", "To compress build output"],
        "correct": 1,
        "explanation": "maven-enforcer-plugin validates build requirements: Java version (requireJavaVersion), Maven version (requireMavenVersion), banned dependencies (bannedDependencies), and dependency convergence across modules."
      }
    ],
    "codingExercise": {
      "instruction": "Create a multi-module Maven project with three modules: (1) an 'api' module with a public interface, (2) a 'service' module that implements the interface (depends on api), (3) a 'web' module with a main class (depends on service). Use a parent POM to manage dependency versions centrally. Build with mvn install and verify all modules compile.",
      "hint": "Root pom.xml has <packaging>pom</packaging> and <modules> listing the three modules. Each child POM has <parent> referencing the root. api module has no dependencies. service depends on api. web depends on service.",
      "checkKeywords": ["parent", "module", "modules", "packaging>pom", "dependency", "mvn install"]
    }
  }
]
