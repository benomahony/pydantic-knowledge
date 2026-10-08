# `pydantic_ai.workspaces`

Workspace API, backend protocols, and implementations.# `pydantic_ai.workspaces.conformance`

The conformance suite for Pydantic AI workspace backends.

Subclass `WorkspaceBackendSuite` in a pytest module and provide a `backend` fixture: each test checks
one rule of the `WorkspaceBackend` contract, the same rules the built-in and provider backends pass.
Requires pytest and the anyio pytest plugin.



### `WorkspaceBackendSuite`

```python
class WorkspaceBackendSuite
```


Subclass in your test suite and provide the `backend` fixture.

Each test checks one rule of the backend contract. Command rules skip for a backend without
`SupportsCommands`; filesystem rules run through [`Workspace`][pydantic_ai.workspaces.Workspace], so a
command-only backend is checked on the file operations derived through its shell. The reattach
rules need the optional fixtures below and skip without them.

#### `fresh_backend`

```python
def fresh_backend(self) -> Callable[[], WorkspaceBackend] | None
```


Build an uninitialized backend to check concurrent first use, if supported.

#### `destructive_backend`

```python
def destructive_backend(self, fresh_backend: Callable[[], WorkspaceBackend] | None) -> Callable[[], WorkspaceBackend] | None
```


Build an independent environment for destruction; defaults to `fresh_backend`.

#### `attach_backend`

```python
def attach_backend(self) -> Callable[[WorkspaceRef], WorkspaceBackend] | None
```


Build a second backend that attaches to `ref`. Enables the reattach rules.

#### `destroy_environment`

```python
def destroy_environment(self) -> Callable[[WorkspaceBackend], Awaitable[None]] | None
```


Destroy the environment behind `backend`. Enables the reattach-after-destroy rule.

#### `test_command_form_must_match_shell`

```python
async def test_command_form_must_match_shell(self, backend: WorkspaceBackend) -> None
```


A string needs `shell=True` and an argv sequence needs `shell=False`; a mismatch is a `TypeError`.

#### `test_stdin_is_at_eof`

```python
async def test_stdin_is_at_eof(self, backend: WorkspaceBackend) -> None
```


Noninteractive commands never wait for input from the caller.

#### `test_command_output_is_complete`

```python
async def test_command_output_is_complete(self, backend: WorkspaceBackend) -> None
```


If output cannot be collected in full, the backend must raise rather than return a truncated success.

#### `can_detect_exit_with_inherited_output_pipes`

```python
def can_detect_exit_with_inherited_output_pipes(self) -> bool
```


Override only if the SDK cannot report exit independently of pipe EOF (E2B currently cannot).

#### `test_result_reports_exit_code_stdout_and_stderr`

```python
async def test_result_reports_exit_code_stdout_and_stderr(self, backend: WorkspaceBackend) -> None
```


A non-zero exit is a normal result, not an error.

#### `test_a_missing_program_exits_127`

```python
async def test_a_missing_program_exits_127(self, backend: WorkspaceBackend) -> None
```


Like `sh`, a program that doesn't exist is a normal result with exit code 127, not an error.

#### `test_working_dir_is_canonical`

```python
async def test_working_dir_is_canonical(self, backend: WorkspaceBackend) -> None
```


Absolute, symlinks resolved, no `.`/`..`: the directory commands actually start in.

#### `test_large_file_round_trip`

```python
async def test_large_file_round_trip(self, backend: WorkspaceBackend) -> None
```


A shell-derived filesystem must page reads rather than hit a command-output cap.

#### `has_real_posix_shell`

```python
def has_real_posix_shell(self) -> bool
```


Only a test double with no POSIX process/filesystem can opt out.

#### `enforces_parent_file_errors`

```python
def enforces_parent_file_errors(self) -> bool
```


Opt out only for an in-memory test double without real path traversal.

#### `filesystem_honors_shell_permissions`

```python
def filesystem_honors_shell_permissions(self) -> bool
```


Override only for provider file APIs that bypass the command user's permissions (e.g. E2B envd).

#### `test_native_realpath_keeps_the_working_dir_and_missing_names`

```python
async def test_native_realpath_keeps_the_working_dir_and_missing_names(self, backend: WorkspaceBackend) -> None
```


Checked without commands, so a filesystem-only backend's `realpath` is covered too.

#### `test_a_backend_attached_by_ref_reaches_the_same_environment`

```python
async def test_a_backend_attached_by_ref_reaches_the_same_environment(self, backend: WorkspaceBackend, attach_backend: Callable[[WorkspaceRef], WorkspaceBackend] | None) -> None
```


Durable execution rebuilds the backend from its ref for every call, so this is what it relies on.