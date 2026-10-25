"""Swift source selection must include app and test code without UI assets."""

from coding_review.sources import load_files


def test_swift_snapshot(tmp_path):
    (tmp_path / "App.swift").write_text("import UIKit\n")
    (tmp_path / "AppTests.swift").write_text("import XCTest\n")
    (tmp_path / "Screen.storyboard").write_text("<document/>")
    assert load_files(tmp_path) == {
        "App.swift": "import UIKit\n",
        "AppTests.swift": "import XCTest\n",
    }
