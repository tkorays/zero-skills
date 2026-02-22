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

### Search Skills

```bash
npx skills find "[query]"
```

### Install a Skill

```bash
# Install globally
npx skills add [package] -g -y

# Install from GitHub
npx skills add [owner]/[repo] -g -y
```

### List Installed Skills

```bash
npx skills list -g
```

### Uninstall a Skill

```bash
npx skills remove [package] -g
```

## Publishing Your Skills

To publish your skills to GitHub:

1. Create a GitHub repository
2. Push your skills to GitHub
3. Others can install using:
   ```bash
   npx skills add [owner]/[repo] -g -y
   ```

## Skill Format

Each skill should include:
- **Name**: Clear, descriptive name
- **Description**: What the skill does
- **Instructions**: How to use the skill
- **Examples**: Real-world usage examples

## License

MIT
