from decky_plugin import DeckyPlugin, logger
import subprocess

class Plugin:
    async def get_power_state(self) -> dict:
        try:
            output = subprocess.check_output(["cat", "/sys/class/power_supply/BAT1/uevent"], text=True)
            result = {}
            for line in output.strip().split("\n"):
                key, _, value = line.partition("=")
                result[key] = value
            return result
        except Exception as e:
            logger.error(f"Error leyendo el estado de energía: {e}")
            return {"error": str(e)}
