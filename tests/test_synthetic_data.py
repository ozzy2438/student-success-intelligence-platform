import subprocess
import sys


def test_synthetic_generator_runs():
    result = subprocess.run(
        [sys.executable, "-m", "src.generate_synthetic_data"],
        capture_output=True,
        text=True,
        check=False,
    )
    assert result.returncode == 0, result.stderr
    assert "Synthetic data generation completed successfully" in result.stdout
