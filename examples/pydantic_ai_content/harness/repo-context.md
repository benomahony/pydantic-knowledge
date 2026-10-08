---
title: Repo Context
description: "Load a repo's AGENTS.md and CLAUDE.md instruction files into a Pydantic AI agent and inventory its skills, subagents, and hooks under .claude or .agents."
---

# Repo Context

`RepoContext` discovers and loads a repo's accumulated coding-assistant context engineering (CE): the instruction files (`CLAUDE.md`/`AGENTS.md`) scattered across the tree and the assets under `.claude`/`.agents`/`.codex`/`.grok` (skills, sub-agents, hooks).

[Source](https://github.com/pydantic/pydantic-ai/tree/main/src/pydantic_ai_harness/pydantic_ai_harness/repo_context/)

> While Pydantic AI Harness is on 0.x releases, the API may change between minor releases; when it does, deprecation warnings and release-note migration guidance tell you (or your agent) exactly how to upgrade. See the [version policy](index.md#version-policy).

## The problem

A repo accumulates CE for whatever coding assistant worked in it: instruction files (`CLAUDE.md`/`AGENTS.md`) scattered across the tree, and assets under `.claude`/`.agents`/`.codex`/`.grok` (skills, sub-agents, hooks). An agent that loads only the top-level instruction file misses the ancestor context and has no idea the rest of the setup exists, so it cannot honor all of it.

## The solution

`RepoContext` bundles three strategies, each independently toggleable. Construct it with `RepoContext(...)` in an `Agent`'s `capabilities`, with a workspace attached to the run:

```python
from pathlib import Path

from pydantic_ai import Agent
from pydantic_ai.capabilities import LocalWorkspace
from pydantic_ai_harness import RepoContext

agent = Agent(
    'anthropic:claude-opus-5-5',
    capabilities=[LocalWorkspace('.'), RepoContext(home_dir=Path.home())],
)

result = agent.run_sync('Summarize the coding-assistant setup in this repo.')
print(result.output)
```

`RepoContext` reads from the run's [workspace](https://pydantic.dev/docs/ai/core-concepts/workspace/), starting at its working directory. To point it at a subdirectory, set it on the workspace: `LocalWorkspace('./repo')`. `home_dir` and `asset_roots` are paths in the workspace: relative ones resolve from the working directory, and `~` is not expanded. A run without a workspace fails at its start.

### 1. Walk-up instruction autoload (on by default)

Loads `CLAUDE.md`/`AGENTS.md` from the working directory and every ancestor up to `home_dir` (inclusive). Precedence is ancestor-first, workspace-last: broadest context first, most specific last. Files are deduped by visited path and by content hash, so a symlinked `AGENTS.md -> CLAUDE.md` or two ancestors sharing identical content load once. Symlinks to instruction files outside the directory being scanned are skipped, including shared dotfiles in another directory.

When `home_dir` is `None` (the default), only the working directory is scanned -- no walk-up. Pass the workspace home path explicitly to walk up to it. For a remote sandbox, use its home (for example `home_dir='/home/user'` on E2B), not the agent host's `Path.home()`.

### 2. Asset inventory (off by default)

Set `expose_inventory_tool=True` to expose `inventory_agent_context()`, which reports where the repo's CE assets live -- the `.claude`/`.agents`/`.codex`/`.grok` roots and, within each, the `skills/` (`SKILL.md`), `agents/` (`.md`), and `settings.json` (hooks) it contains. It returns a structured `AgentContextInventory`; it locates assets and does not parse them.

Rename the tool with `inventory_tool_name`, or scope which roots it scans with `asset_roots`.
Skill discovery goes at most eight directories deep.

### 3. Nested-on-traversal (off by default)

When the model lists or reads a directory, surface that directory's
`CLAUDE.md`/`AGENTS.md`. This strategy subscribes to `FileReadEvent` and
`DirectoryListedEvent`, so it receives normalized, containment-checked paths
instead of inspecting raw tool arguments. It remains opt-in:

```python
from pydantic_ai import Agent
from pydantic_ai.capabilities import LocalWorkspace
from pydantic_ai_harness import FileSystem, RepoContext

agent = Agent(
    'anthropic:claude-opus-5-5',
    capabilities=[
        LocalWorkspace('.'),
        FileSystem(),
        RepoContext(
            nested_traversal=True,
            nested_inject='pointer',  # or 'contents'
        ),
    ],
)
result = agent.run_sync('List the source directory.')
```

`nested_inject='pointer'` (default) enqueues a one-line note pointing at the
file; `'contents'` enqueues the file body. The note reaches message history
before the next model request. Each directory is surfaced at most once per run.

`FileSystem` emits these events directly. Hosts with other file tools can emit
the same types by importing `FileReadEvent` and `DirectoryListedEvent` from
`pydantic_ai_harness.filesystem`; set `root_dir` to the directory the event's
`path` is relative to.

The traversed location is `root_dir / path`, so a `FileSystem` rooted at a
subdirectory of the working directory still surfaces the right directory. A
traversal that resolves outside the working directory is ignored: it is not nested in
the workspace, so there is no nested context to surface.

`traversal_tool_names` and `traversal_path_arg` are deprecated. Setting either
to a non-default value emits `HarnessDeprecationWarning` and keeps the old
tool-name and argument sniffing path active for hosts that do not emit events.
With the defaults, sniffing is disabled, so a `FileSystem` event cannot deliver
the same note twice.

## Cache cost

Injecting file contents into the system prompt costs prompt-cache stability: a changed prefix re-bills the whole cached region. `RepoContext` keeps the two cache-relevant paths separate:

- Strategy 1 reads its files once at run start and injects them as static system instructions, so the cached prefix stays byte-identical across turns.
- Strategy 3 is volatile (it depends on which directory was just touched), so its note is enqueued in the message tail, never in the system prompt, and cannot invalidate the cached prefix.

## Configuration

```python {test="skip"}
RepoContext(
    home_dir=None,                  # str | Path | None -- shallowest workspace dir to stop walk-up at, inclusive
    filenames=('CLAUDE.md', 'AGENTS.md'),
    autoload_instructions=True,     # Strategy 1
    expose_inventory_tool=False,    # Strategy 2
    inventory_tool_name='inventory_agent_context',
    nested_traversal=False,         # Strategy 3
    nested_inject='pointer',        # 'pointer' | 'contents'
    traversal_tool_names=frozenset({'list_directory', 'read_file'}),  # deprecated fallback
    traversal_path_arg='path',                                       # deprecated fallback
    asset_roots=('.claude', '.agents', '.codex', '.grok'),
)
```

`workspace_dir=` is deprecated and ignored: the working directory comes from the workspace.

## Scope

`RepoContext` locates and loads CE; it does not parse skill/sub-agent frontmatter or hook bodies, and it does not modify assets. Strategy 1 reads its files once per run, so mid-run edits to those files are not reloaded.

## Further reading

- [Pydantic AI capabilities](../capabilities/overview.md)
- [Pydantic AI hooks](../hooks.md)

## API reference

## `RepoContext`

```python
class RepoContext
```


Discover and load a repo's accumulated coding-assistant context engineering.

Three strategies, each independently toggleable:

Everything is read through the run's workspace, anchored at its working
directory; a run without a workspace fails at its start.

1. Walk-up instruction autoload (`autoload_instructions`, on by default):
   load `CLAUDE.md`/`AGENTS.md` from the working directory and every ancestor
   up to `home_dir`, deduped, ancestor-first. These are read once at run start
   and injected as **static system instructions** via `get_instructions`, so
   they stay in the cached prefix and never re-read per turn.

2. Asset inventory (`expose_inventory_tool`, off by default): a tool that
   reports where the repo's CE assets live (`.claude`/`.agents`/`.codex`/
   `.grok` and their `skills/`, `agents/`, `settings.json`). It locates
   assets; it does not parse them.

3. Nested-on-traversal (`nested_traversal`, off by default): when the model
   lists or reads a directory through a filesystem capability event,
   surface that directory's `CLAUDE.md`/`AGENTS.md`. The note is enqueued in
   the message tail, not added to system instructions, so it does not
   invalidate the cached prefix. `nested_inject='pointer'` (default)
   enqueues a one-line pointer; `'contents'` inlines the file body.

Cache note: injecting file contents into the system prompt costs prompt-cache
stability. Strategy 1 is safe because its files are static; the volatile
Strategy 3 content rides in the message tail instead.

```python
from pathlib import Path

from pydantic_ai import Agent
from pydantic_ai.capabilities import LocalWorkspace
from pydantic_ai_harness.repo_context import RepoContext

agent = Agent(
    'anthropic:claude-sonnet-4-6',
    capabilities=[LocalWorkspace('.'), RepoContext(home_dir=Path.home())],
)
```

```python
workspace_dir: Path | None = None
```

```python
home_dir: str | Path | None = None
```

```python
filenames: Sequence[str] = ('CLAUDE.md', 'AGENTS.md')
```

```python
autoload_instructions: bool = True
```

```python
expose_inventory_tool: bool = False
```

```python
inventory_tool_name: str = 'inventory_agent_context'
```

```python
nested_traversal: bool = False
```

```python
nested_inject: Literal['pointer', 'contents'] = 'pointer'
```

```python
traversal_tool_names: frozenset[str] = _DEFAULT_TRAVERSAL_TOOL_NAMES
```

```python
traversal_path_arg: str = _DEFAULT_TRAVERSAL_PATH_ARG
```

```python
asset_roots: Sequence[str] = ('.claude', '.agents', '.codex', '.grok')
```

```python
_context_files: list[ContextFile] | None = field(default=None, init=False, repr=False, compare=False)
```

```python
_seen_dirs: set[str] = field(default_factory=set[str], init=False, repr=False, compare=False)
```

```python
_cached_working_dir: Path | None = field(default=None, init=False, repr=False, compare=False)
```

```python
_toolset: RepoContextToolset[AgentDepsT] | None = field(default=None, init=False, repr=False, compare=False)
```

```python
_sniff_traversal_tools: bool = field(default=False, init=False, repr=False, compare=False)
```

### `for_run`

```python
async def for_run(self, ctx: RunContext[AgentDepsT]) -> RepoContext[AgentDepsT]
```


Return a fresh per-run instance with isolated traversal/cache state.

The copy skips `__post_init__`, so deprecated arguments warned about at construction are not warned again.

### `before_run`

```python
async def before_run(self, ctx: RunContext[AgentDepsT]) -> None
```


Fail without a workspace, and load walk-up instruction files so `get_instructions` is sync.

### `get_instructions`

```python
def get_instructions(self) -> str | Callable[[RunContext[AgentDepsT]], str | None] | None
```


Cache-stable instructions resolved after `before_run` loads workspace files.

### `get_toolset`

```python
def get_toolset(self) -> AgentToolset[AgentDepsT] | None
```


The asset-inventory toolset, or `None` when the tool is disabled.

### `after_tool_execute`

```python
async def after_tool_execute(self, ctx: RunContext[AgentDepsT], *, call: ToolCallPart, tool_def: ToolDefinition, args: dict[str, Any], result: Any) -> Any
```


Support customized legacy traversal tool and argument names.



### `get_serialization_name`

```python
def get_serialization_name(cls) -> str | None
```


Serialization name for agent-spec support.## `AgentContextInventory`

```python
class AgentContextInventory
```


A map of where a repo's CE assets live, for an orchestrator to inspect.

```python
roots: list[AssetRoot] = Field(default_factory=list[AssetRoot], description='One entry per scanned root directory.')
```## `AssetRoot`

```python
class AssetRoot
```


Where CE assets live under a single root directory (e.g. `.claude`).

```python
root: str = Field(description='The root directory name, relative to the workspace, e.g. ".claude".')
```

```python
exists: bool = Field(description='Whether the root directory is present in the workspace.')
```

```python
skills: list[str] = Field(default_factory=list, description='Paths to SKILL.md files found under skills/.')
```

```python
agents: list[str] = Field(default_factory=list, description='Paths to agent .md files found under agents/.')
```

```python
settings: str | None = Field(default=None, description='Path to settings.json (hooks), if present.')
```