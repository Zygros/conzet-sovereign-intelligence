import unittest
from scripts.validate_skill_frontmatter import validate_skill_text

class SkillFrontmatterTests(unittest.TestCase):
    def test_valid_skill(self):
        self.assertEqual(validate_skill_text("---\nname: test-skill\ndescription: A test skill.\n---\n\n# Instructions\nDo the thing."), [])
    def test_missing_frontmatter(self):
        self.assertTrue(validate_skill_text("# No frontmatter"))
    def test_bad_name(self):
        errors = validate_skill_text("---\nname: Bad_Name\ndescription: Desc\n---\nBody")
        self.assertTrue(any("lowercase hyphen-separated" in x for x in errors))
    def test_empty_body(self):
        errors = validate_skill_text("---\nname: valid-name\ndescription: Desc\n---\n")
        self.assertTrue(any("missing skill instructions" in x for x in errors))
    def test_duplicate_field(self):
        errors = validate_skill_text("---\nname: first\nname: second\ndescription: Desc\n---\nBody")
        self.assertTrue(any("duplicate frontmatter" in x for x in errors))

if __name__ == "__main__":
    unittest.main()