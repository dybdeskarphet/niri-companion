# Configuration

`niri-ipcext` only requires the `general.output_path` (usually `config.kdl`) to be set in order to work.

It works by replacing strings directly in your `general.output_path` file.

> [!NOTE]
> Since `output_path` is not a temporary file, `niri-ipcext` uses it as the IPC target for modifications.

# Usage

## `niri-ipcext replace`

Replaces a string in your `general.output_path` with another string.

Example: changing your border width. Suppose your config contains:

```kdl
layout {
    ...

    border {
        width 2

        ...
    }

    ...
}
```

Running:

```
niri-ipcext replace 'width 2' 'width 10'
```

Will update the border width to `10`.

> [!TIP]
> Make sure to match the exact string, including spaces, when using `replace`.

## `niri-ipcext restore`

Restores your default configuration by regenerating `config.kdl`:

```
niri-ipcext restore
```

This simply runs:

```
niri-genconfig generate
```
