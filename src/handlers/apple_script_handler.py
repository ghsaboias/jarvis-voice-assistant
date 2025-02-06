import logging
import subprocess
from typing import Optional, Tuple


class AppleScriptHandler:
    @staticmethod
    def run_script(script: str) -> Tuple[bool, Optional[str], Optional[str]]:
        """
        Executes an AppleScript and returns success status and output

        Returns:
            tuple: (success, stdout, stderr)
        """
        try:
            result = subprocess.run(
                ["osascript", "-e", script], capture_output=True, text=True
            )
            return (
                (True, result.stdout.strip(), result.stderr.strip())
                if result.returncode == 0
                else (False, None, result.stderr.strip())
            )
        except Exception as e:
            logging.error(f"AppleScript execution failed: {e}")
            return False, None, str(e)

    @staticmethod
    def tell_app(app: str, command: str) -> Tuple[bool, Optional[str], Optional[str]]:
        """Executes a command in the context of an application"""
        script = f'tell application "{app}"\n{command}\nend tell'
        return AppleScriptHandler.run_script(script)
