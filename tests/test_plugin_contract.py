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

    def test_mcp_configuration_uses_public_server_with_pre_registered_oauth(self):
        config = self.load_json(PLUGIN / ".mcp.json")
        server = config["mcpServers"]["hdnavigator"]

        self.assertEqual(set(server), {"type", "url", "oauth"})
        self.assertEqual(server["type"], "http")
        self.assertEqual(server["url"], "https://mcp.slavayank.com/mcp")
        self.assertEqual(server["oauth"]["clientId"], "hdnavigator-mcp")
        self.assertEqual(server["oauth"]["callbackUrl"], "http://127.0.0.1/callback")

    def test_skill_instructions_cover_required_workflows(self):
        skill = (PLUGIN / "skills" / "hdnavigator-chart-guide" / "SKILL.md").read_text(
            encoding="utf-8"
        )

        for expected in [
            "get_new_chart",
            "list_saved_charts",
            "get_saved_chart",
            "hdn_",
            "token",
            "chat",
            "HDNAVIGATOR_MCP_TOKEN",
            "image_url",
            "![Human Design bodygraph]",
            "limit",
            "offset",
            "402",
            "translate",
            "setx",
            "environment variable",
            "OAuth",
            "codex mcp login",
            "opencode mcp auth",
            "own browser",
            "Authorization",
        ]:
            self.assertIn(expected, skill)

        self.assertIn("Never repeat the token", skill)

    def test_readme_explains_all_three_authentication_flows(self):
        readme = (ROOT / "README.md").read_text(encoding="utf-8")

        self.assertIn("hdn_", readme)
        self.assertIn("HDNAVIGATOR_MCP_TOKEN", readme)
        self.assertIn("https://hdnavigator.ru", readme)
        self.assertIn("setx", readme)
        self.assertIn("codex mcp login", readme)
        self.assertIn("opencode mcp auth", readme)
        self.assertIn("own browser", readme)
        self.assertIn("Authorization", readme)
        self.assertIn("dual-mode", readme)

    def test_readme_has_codex_and_opencode_setup_examples(self):
        readme = (ROOT / "README.md").read_text(encoding="utf-8")

        self.assertIn("bearer_token_env_var", readme)
        self.assertIn("opencode mcp add hdnavigator", readme)
        self.assertIn("{env:HDNAVIGATOR_MCP_TOKEN}", readme)

    def test_marketplace_entry_is_installable_on_install(self):
        marketplace = self.load_json(ROOT / ".agents" / "plugins" / "marketplace.json")
        [entry] = marketplace["plugins"]

        self.assertEqual(marketplace["name"], "hdnavigator")
        self.assertEqual(marketplace["interface"]["displayName"], "HDnavigator")
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
