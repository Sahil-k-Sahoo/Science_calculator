import subprocess
import sys
import unittest
from pathlib import Path

REPO_DIR=Path(__file__).resolve().parent.parent


class TestCli(unittest.TestCase):
    def test_piped_input_and_errors(self) -> None:
        script_input="\n2 ^ 3 ^ 2\ntotient(9)\n1 / 0\nexit\n"
        proc=subprocess.run(
            [sys.executable,"scicalc.py"],
            cwd=REPO_DIR,
            input=script_input,
            text=True,
            capture_output=True,
            timeout=10,
        )
        self.assertEqual(proc.returncode,0)
        self.assertNotIn("SciCalc>",proc.stdout)
        self.assertNotIn("Traceback",proc.stdout)
        self.assertNotIn("Traceback",proc.stderr)
        lines=[line.strip() for line in proc.stdout.splitlines() if line.strip()]
        self.assertEqual(lines[0],"512.0")
        self.assertEqual(lines[1],"6")
        self.assertTrue(lines[2].startswith("[ERROR]"))


if __name__ == "__main__":
    unittest.main()