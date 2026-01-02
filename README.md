# Claude Store

A collection of techniques, patterns, and tools for working effectively with Claude Code.

## Overview

This repository contains my personal collection of Claude-related techniques and configurations. It's an evolving project that captures best practices, custom commands, specialized agents, and skills developed through extensive hands-on experience with Claude.

## What's Inside

This collection focuses on practical techniques for:

- **Agent Design Patterns**: Reusable agent architectures for common tasks
- **Custom Commands**: Slash commands that extend Claude's capabilities
- **Specialized Skills**: Domain-specific expertise and workflows
- **Prompt Engineering**: Techniques for getting the best results from Claude

## Usage

### Agents

Place agent configuration files in the `agents/` directory. These subagent configurations can be launched using the Task tool in Claude Code:

```
Use the Task tool with the subagent_type parameter matching your agent configuration
```

Agents are ideal for complex, multi-step tasks that require specialized capabilities or autonomous execution.

### Commands

Place custom slash command definitions in the `commands/` directory. Each command file (`.md` format) defines a slash command that you can invoke directly:

```
/command-name
```

Commands are perfect for frequently-used workflows, predefined prompts, or complex operations you want to repeat consistently.

### Skills

Place skill definitions in the `skills/` directory. Skills extend Claude's capabilities with specialized knowledge and workflows:

```
Use the Skill tool to invoke a skill by name
```

Skills are designed for domain-specific tasks like document processing, data analysis, or specialized content creation.

## Philosophy

The techniques shared here are grounded in real-world usage. Each pattern, command, or skill has been developed and refined through actual work, not theoretical exploration.

The goal is to share practical, immediately useful approaches that you can adapt to your own needs.

## Status

This is the initial version of the repository. The content will evolve and expand as I continue to discover and refine new techniques.

## Contributing

While this is primarily a personal collection, feel free to explore, adapt, and use these techniques in your own work. If you find something particularly useful, I'd love to hear about it.

---

*Last updated: January 2026*
