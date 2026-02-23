# My LLM Skills

A collection of custom skills/prompts for LLMs.

## Skills

This repository contains custom skills that can be used with LLMs to enhance productivity and provide specialized capabilities.

### Structure

```
skills/
├── README.md           # Skills index
└── example/            # Example skill (rename/delete)
    ├── skill.md        # Skill definition
    └── examples/       # Example usage
```

### Adding a New Skill

1. Create a new folder under `skills/`
2. Add `skill.md` with the skill definition
3. (Optional) Add `examples/` with usage examples
4. Update `skills/README.md` with the new skill

## Installation & Usage

This repository can be used with the `npx skills` CLI tool. Make sure you have Node.js installed.

### Available Skills

| Skill Name | Description |
|------------|-------------|
| `data-analyze-with-sql-python` | SQL, pandas, and Python data analysis for queries, data cleaning, and exploratory analysis |
| `feishu-docx-python` | Create and manipulate Feishu/Lark cloud documents using Python SDK |
| `install-skills-for-personal-work` | Automatically install all personal development skills in a fresh environment |
| `xtquant` | XtQuant Python量化交易库，获取行情数据、实盘交易、查询财务数据 |

### Install Skills

Since this is a multi-skill repository, use the `--skill` flag to install specific skills:

```bash
# Install a single skill
npx skills add tkorays/zero-skills --skill data-analyze-with-sql-python -g -y

# Install multiple skills at once
npx skills add tkorays/zero-skills --skill data-analyze-with-sql-python --skill feishu-docx-python --skill xtquant -g -y

# Install all skills
npx skills add tkorays/zero-skills --skill data-analyze-with-sql-python --skill feishu-docx-python --skill install-skills-for-personal-work --skill xtquant -g -y
```

### List Installed Skills

```bash
npx skills list -g
```

### Uninstall a Skill

```bash
npx skills remove data-analyze-with-sql-python -g
npx skills remove feishu-docx-python -g
npx skills remove install-skills-for-personal-work -g
npx skills remove xtquant -g
```

## Publishing Your Skills

This repository is already published on GitHub at: https://github.com/tkorays/zero-skills

Others can install your skills using:

```bash
npx skills add tkorays/zero-skills --skill [skill-name] -g -y
```

## Skill Format

Each skill in this repository includes:
- **Name**: Clear, descriptive name
- **Description**: What the skill does and when to use it
- **Instructions**: How to use the skill
- **Examples**: Real-world usage examples and code snippets

## License

MIT
