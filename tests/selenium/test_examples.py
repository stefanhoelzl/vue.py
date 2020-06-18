import time

from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys


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


def test_grid_component(selenium):
    with selenium.example():
        time.sleep(0.5)
        query = selenium.element_present("query")
        query.clear()
        query.send_keys("j")
        power = selenium.element_present("power")
        power.click()
        rows = selenium.driver.find_elements_by_tag_name("td")
        assert "Jet Li" == rows[0].text
        assert "8000" == rows[1].text
        assert "Jackie Chan" == rows[2].text
        assert "7000" == rows[3].text


def test_tree_view(selenium):
    with selenium.example():
        time.sleep(0.5)
        lis = selenium.find_elements_by_tag_name("li")
        lis[0].click()
        lis[3].click()
        ActionChains(selenium.driver).double_click(lis[8]).perform()
        assert selenium.find_elements_by_tag_name("li")[9].text == "new stuff"


def test_svg_graph(selenium):
    with selenium.example():
        time.sleep(0.5)
        selenium.find_elements_by_tag_name("button")[5].click()

        a = selenium.find_elements_by_tag_name("input")[0]
        d = selenium.find_elements_by_tag_name("input")[3]
        ActionChains(selenium.driver).click_and_hold(a).move_by_offset(
            20, 0
        ).release().perform()

        ActionChains(selenium.driver).click_and_hold(d).move_by_offset(
            5, 0
        ).release().perform()

        polygon = selenium.find_elements_by_tag_name("polygon")[0]
        assert 5 == len(polygon.get_attribute("points").split(" "))


def test_modal_component(selenium):
    with selenium.example():
        time.sleep(1)
        show_button = selenium.element_present("show-modal")
        show_button.click()
        time.sleep(1)
        assert selenium.element_present("modal_view", timeout=2)


def test_todo_mvc(selenium):
    with selenium.example():
        time.sleep(0.5)
        title_input = selenium.element_present("title-input")
        title_input.clear()
        title_input.send_keys("new todo")
        title_input.send_keys(Keys.ENTER)
        title_input.send_keys("completed")
        title_input.send_keys(Keys.ENTER)

        toggle_buttons = selenium.driver.find_elements_by_class_name("toggle")
        assert 2 == len(toggle_buttons)

        toggle_buttons[1].click()
        selenium.element_present("show-active").click()
        labels = selenium.driver.find_elements_by_tag_name("label")
        assert 1 == len(labels)
        assert "new todo" == labels[0].text

        selenium.element_present("show-all").click()
        labels = selenium.driver.find_elements_by_tag_name("label")
        assert 2 == len(labels)
        assert "new todo" == labels[0].text
        assert "completed" == labels[1].text


def test_github_commits(selenium):
    with selenium.example(hash_="testing"):
        assert selenium.element_with_tag_name_present("ul")
        time.sleep(2)
        assert 10 == len(selenium.driver.find_elements_by_tag_name("li"))


def test_elastic_header(selenium):
    with selenium.example():
        assert selenium.element_present("header")
        header = selenium.find_element_by_id("header")
        content = selenium.find_element_by_id("content")

        assert (
            content.get_attribute("style") == "transform:"
            " translate3d(0px, 0px, 0px);"
        )

        ActionChains(selenium.driver).click_and_hold(header).move_by_offset(
            xoffset=0, yoffset=100
        ).perform()
        selenium.screenshot()
        assert (
            content.get_attribute("style") == "transform:"
            " translate3d(0px, 33px, 0px);"
        )

        ActionChains(selenium.driver).release().perform()
        time.sleep(1)
        assert (
            content.get_attribute("style") == "transform:"
            " translate3d(0px, 0px, 0px);"
        )
