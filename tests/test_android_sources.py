"""Android language and build-file selection."""

from coding_review.sources import load_files


def test_android_source_and_build_selection(tmp_path):
    expected = {
        "Main.java": "class Main {}",
        "Security.kt": "class Security",
        "build.gradle": "plugins {}",
        "settings.gradle.kts": 'rootProject.name = "App"',
    }
    for name, text in expected.items():
        (tmp_path / name).write_text(text)
    (tmp_path / "strings.xml").write_text("<resources/>")
    assert load_files(tmp_path) == expected
