import pathlib
import subprocess
import asyncio
import os

HOME_DIR = str(pathlib.Path(os.getcwd()).parent.parent.resolve())
PARENT_DIR = str(pathlib.Path(__file__).parent.resolve())

class Plugin:
    backend_proc = None
    # Asyncio-compatible long-running code, executed in a task when the plugin is loaded
    async def _main(self):
        # startup
        print("PowerTools starting...")
        env_proc = dict(os.environ)
        if "LD_LIBRARY_PATH" in env_proc:
            env_proc["LD_LIBRARY_PATH"] += ":"+PARENT_DIR+"/bin"
        else:
            env_proc["LD_LIBRARY_PATH"] = ":"+PARENT_DIR+"/bin"
        self.backend_proc = subprocess.Popen(
            [PARENT_DIR + "/bin/backend"],
            env = env_proc)
        while True:
            await asyncio.sleep(1)

    async def _unload(self):
        # shutdown
        print("PowerTools unloading...")
        if self.backend_proc is not None:
            self.backend_proc.terminate()
            try:
                self.backend_proc.wait(timeout=5) # 5 seconds timeout
            except subprocess.TimeoutExpired:
                self.backend_proc.kill()
            self.backend_proc = None
import { definePlugin, PanelSection, ServerAPI, staticClasses } from "decky-frontend-lib";
import { VFC, useEffect, useState } from "react";

const Content: VFC<{ serverAPI: ServerAPI }> = ({ serverAPI }) => {
  const [powerData, setPowerData] = useState<any>(null);

  useEffect(() => {
    serverAPI.callPluginMethod("get_power_state", {}).then(({ result }) => {
      setPowerData(result);
    });
  }, []);

  return (
    <PanelSection title="Estado de Energía">
      {powerData ? (
        <div className={staticClasses.Text}>{JSON.stringify(powerData, null, 2)}</div>
      ) : (
        <div className={staticClasses.Text}>Cargando...</div>
      )}
    </PanelSection>
  );
};

export default definePlugin((serverAPI) => {
  return {
    title: "PowerTools ROG Ally",
    content: <Content serverAPI={serverAPI} />, 
    icon: <img src="decky-plugin://powertools-rog-ally/icon.png" />
  };
});
