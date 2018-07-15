import time


def test_markdown_editor(selenium):
    with selenium.example():
        time.sleep(0.5)
        element = selenium.element_present("markdown")
        element.clear()
        element.send_keys("# Title\n\n")
        element.send_keys("* item one\n")
        element.send_keys("* item two\n")
        element.send_keys("\n")
        element.send_keys("_italic_\n")
        element.send_keys("\n")
        element.send_keys("`some code`\n")
        element.send_keys("\n")
        element.send_keys("**bold**\n")
        element.send_keys("\n")
        element.send_keys("## Sub Title\n")
        element.send_keys("\n")
        selenium.element_has_text("sub-title", "Sub Title")
