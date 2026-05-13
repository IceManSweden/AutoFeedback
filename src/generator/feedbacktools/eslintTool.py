import subprocess


def run_eslint(dir=".") -> dict:
    """Runs Eslint on a directory

    Args:
        dir: The directory path

    Returns:
        The result of running eslint
    """
    res = subprocess.run(
        ["npx", "eslint", dir],
        capture_output=True,
        encoding="utf-8",
        text=True,
    )

    return {
        "exit_code": res.returncode,
        "stdout": res.stdout,
        "stderr": res.stderr,
    }


if __name__ == "__main__":
    run_eslint()
