# 🤖 agent-swarm-cli

> A tiny team of specialist robots, one per CLI tool, coordinated by a Boss Robot.
> You ask in plain English. The Boss picks the right helper. The helper runs the command.

## What it does

```
You  ──►  Boss Robot (Orchestrator)  ──►  Git Robot   ──►  runs `git ...`
                                    ├──►  Docker Robot ──►  runs `docker ...`
                                    ├──►  Kube Robot   ──►  runs `kubectl ...`
                                    ├──►  NPM Robot    ──►  runs `npm ...`
                                    ├──►  Pip Robot    ──►  runs `pip ...`
                                    └──►  TF Robot     ──►  runs `terraform ...`
```

Every robot only knows its **one** tool. Safety-first: read-only commands by default, a denylist, and a `--dry-run` flag.

## Quick Start

```bash
git clone https://github.com/YOUR_USERNAME/agent-swarm-cli.git
cd agent-swarm-cli
python -m venv .venv
source .venv/bin/activate      # Windows: .venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env           # only needed if you want --ai mode
```

### Examples

```bash
python cli.py "show me git status"
python cli.py "list docker containers"
python cli.py "list pip packages"
python cli.py "what kubectl context am I on"
python cli.py --dry-run "show git log"
python cli.py --json "git diff"
python cli.py --list-agents
python cli.py "!echo hello world"        # run a literal command (still safety-checked)
python cli.py --ai "what's my current branch"  # needs OPENAI_API_KEY
```

## Flags

| Flag | What it does |
|------|--------------|
| `--dry-run` | Show the command but don't execute it |
| `--json` | Machine-readable output |
| `--ai` | Use OpenAI to route + build the command (needs `OPENAI_API_KEY`) |
| `--list-agents` | Show all available robots |

## The `!` prefix (manual mode)

If you know the exact command, start your request with `!`:

```bash
python cli.py "!git log --oneline -5"
```

It runs literally — but still passes through the global denylist (`rm -rf /`, `mkfs`, `dd if=`, etc.).

## Repo layout

```
agent-swarm-cli/
├── README.md
├── LICENSE
├── requirements.txt
├── .env.example
├── .gitignore
├── Dockerfile
├── docker-compose.yml
├── cli.py
├── swarm/
│   ├── __init__.py
│   ├── orchestrator.py
│   └── agents/
│       ├── __init__.py
│       ├── base.py
│       ├── git_agent.py
│       ├── docker_agent.py
│       ├── kubectl_agent.py
│       ├── npm_agent.py
│       ├── pip_agent.py
│       └── terraform_agent.py
└── tests/
    ├── __init__.py
    └── test_agents.py
```

## Adding your own robot

1. Create `swarm/agents/my_agent.py` — copy `git_agent.py`, rename the class.
2. Override `name`, `keywords`, `allowed_prefixes`, `forbidden_patterns`, and `build_command`.
3. Register it in `swarm/orchestrator.py` (add one line to the agent list).

That's it. The Boss picks it up automatically.

## Sandbox (optional)

Build and run inside Docker so the robots can't hurt your real machine:

```bash
docker compose build
docker compose run --rm swarm python cli.py "show git status"
```

The default image ships with `git`. Add more tools to the `Dockerfile` as you need them.

## Tests

```bash
pytest
```

All tests use `--dry-run`, so no real commands are executed.

## Safety notes

- Never run as `root`.
- Default commands are read-only. Edit the agents if you need write access.
- Review any robot before letting it touch real projects.
- Mounting `/var/run/docker.sock` inside a container is powerful — only do it on machines you trust.

## License

MIT — see `LICENSE`.
