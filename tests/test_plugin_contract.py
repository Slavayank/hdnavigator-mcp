import json
import pathlib
import unittest


ROOT = pathlib.Path(__file__).resolve().parents[1]
PLUGIN = ROOT / "plugins" / "hdnavigator-mcp"


class HDnavigatorPluginContractTests(unittest.TestCase):
    def load_json(self, path):
        return json.loads(path.read_text(encoding="utf-8"))

    def test_manifest_metadata(self):
        manifest = self.load_json(PLUGIN / ".codex-plugin" / "plugin.json")

        self.assertEqual(manifest["name"], "hdnavigator-mcp")
        self.assertEqual(manifest["interface"]["displayName"], "HDnavigator MCP")
        self.assertEqual(manifest["interface"]["websiteURL"], "https://hdnavigator.ru")
        self.assertEqual(manifest["interface"]["capabilities"], ["MCP"])
        self.assertLessEqual(len(manifest["interface"]["defaultPrompt"]), 3)
        self.assertEqual(manifest["interface"]["logo"], "./assets/logo.svg")
        self.assertEqual(manifest["interface"]["composerIcon"], "./assets/logo.svg")

    def test_mcp_configuration_uses_public_server_and_env_token(self):
        config = self.load_json(PLUGIN / ".mcp.json")
        server = config["mcpServers"]["hdnavigator"]

        self.assertEqual(server["type"], "http")
        self.assertEqual(server["url"], "https://mcp.slavayank.com/mcp")
        self.assertEqual(server["bearer_token_env_var"], "HDNAVIGATOR_MCP_TOKEN")

    def test_skill_instructions_cover_required_workflows(self):
        skill = (PLUGIN / "skills" / "hdnavigator-chart-guide" / "SKILL.md").read_text(
            encoding="utf-8"
        )

        for expected in [
            "get_new_chart",
            "list_saved_charts",
            "get_saved_chart",
            "image_url",
            "![Human Design bodygraph]",
            "limit",
            "offset",
            "402",
            "translate",
        ]:
            self.assertIn(expected, skill)

    def test_marketplace_entry_is_installable_on_install(self):
        marketplace = self.load_json(ROOT / ".agents" / "plugins" / "marketplace.json")
        [entry] = marketplace["plugins"]

        self.assertEqual(entry["name"], "hdnavigator-mcp")
        self.assertEqual(entry["source"]["path"], "./plugins/hdnavigator-mcp")
        self.assertEqual(entry["policy"]["installation"], "AVAILABLE")
        self.assertEqual(entry["policy"]["authentication"], "ON_INSTALL")
        self.assertEqual(entry["category"], "Productivity")

    def test_logo_placeholder_exists(self):
        logo = PLUGIN / "assets" / "logo.svg"

        self.assertTrue(logo.exists())
        self.assertIn("<svg", logo.read_text(encoding="utf-8"))


if __name__ == "__main__":
    unittest.main()
