# chat/tests.py
from django.test import TestCase
from .models import Thread, Message
from django.contrib.auth.models import User
from channels.testing import ChannelsLiveServerTestCase
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.wait import WebDriverWait


class ChatTests(ChannelsLiveServerTestCase):
    serve_static = True  # emulate StaticLiveServerTestCase

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        try:
            # NOTE: Requires "chromedriver" binary to be installed in $PATH
            cls.driver = webdriver.Chrome()
        except:
            super().tearDownClass()
            raise

    @classmethod
    def tearDownClass(cls):
        cls.driver.quit()
        super().tearDownClass()

    def test_when_chat_message_posted_then_seen_by_everyone_in_same_room(self):
        try:
            self._enter_chat_room("room_1")

            self._open_new_window()
            self._enter_chat_room("room_1")

            self._switch_to_window(0)
            self._post_message("hello")
            WebDriverWait(self.driver, 2).until(
                lambda _: "hello" in self._chat_log_value,
                "Message was not received by window 1 from window 1",
            )
            self._switch_to_window(1)
            WebDriverWait(self.driver, 2).until(
                lambda _: "hello" in self._chat_log_value,
                "Message was not received by window 2 from window 1",
            )
        finally:
            self._close_all_new_windows()

    def test_when_chat_message_posted_then_not_seen_by_anyone_in_different_room(self):
        try:
            self._enter_chat_room("room_1")

            self._open_new_window()
            self._enter_chat_room("room_2")

            self._switch_to_window(0)
            self._post_message("hello")
            WebDriverWait(self.driver, 2).until(
                lambda _: "hello" in self._chat_log_value,
                "Message was not received by window 1 from window 1",
            )

            self._switch_to_window(1)
            self._post_message("world")
            WebDriverWait(self.driver, 2).until(
                lambda _: "world" in self._chat_log_value,
                "Message was not received by window 2 from window 2",
            )
            self.assertTrue(
                "hello" not in self._chat_log_value,
                "Message was improperly received by window 2 from window 1",
            )
        finally:
            self._close_all_new_windows()

    # === Utility ===

    def _enter_chat_room(self, room_name):
        self.driver.get(self.live_server_url + "/chat/")
        ActionChains(self.driver).send_keys(room_name, Keys.ENTER).perform()
        WebDriverWait(self.driver, 2).until(
            lambda _: room_name in self.driver.current_url
        )

    def _open_new_window(self):
        self.driver.execute_script('window.open("about:blank", "_blank");')
        self._switch_to_window(-1)

    def _close_all_new_windows(self):
        while len(self.driver.window_handles) > 1:
            self._switch_to_window(-1)
            self.driver.execute_script("window.close();")
        if len(self.driver.window_handles) == 1:
            self._switch_to_window(0)

    def _switch_to_window(self, window_index):
        self.driver.switch_to.window(self.driver.window_handles[window_index])

    def _post_message(self, message):
        ActionChains(self.driver).send_keys(message, Keys.ENTER).perform()

    @property
    def _chat_log_value(self):
        return self.driver.find_element(
            by=By.CSS_SELECTOR, value="#chat-log"
        ).get_property("value")


# Create your tests here.


class ThreadTestCase(TestCase):
    def setUp(self):
        self.user1 = User.objects.create_user(
            username='user1', email=None, password='user1234')
        self.user2 = User.objects.create_user(
            username='user2', email=None, password='user2345')
        self.user3 = User.objects.create_user(
            username='user3', email=None, password='user3456')

        self.thread = Thread.objects.create()

    def test_add_user_to_thread(self):
        self.thread.users.add(self.user1, self.user2)

        self.assertEqual(self.thread.users.count(), 2)

    def test_filter_thread_by_user(self):
        self.thread.users.add(self.user1, self.user2)

        thread = Thread.objects.filter(
            users=self.user1).filter(users=self.user2)

        self.assertEqual(self.thread, thread[0])

    def test_filter_non_existent_thread(self):
        thread = Thread.objects.filter(
            users=self.user1).filter(users=self.user2)

        self.assertEqual(thread.count(), 0)

    def test_add_message_to_thread(self):
        self.thread.users.add(self.user1, self.user2)
        message = Message.objects.create(
            user=self.user1, content='test message')
        message2 = Message.objects.create(
            user=self.user2, content='test message 2')

        self.thread.messages.add(message, message2)

        self.assertEqual(self.thread.messages.all().count(), 2)

        for msg in self.thread.messages.all().order_by('id'):
            print("({}):{}".format(msg.user, msg.content))

    def test_add_message_from_user_not_in_thread(self):
        self.thread.users.add(self.user1, self.user2)
        message1 = Message.objects.create(
            user=self.user1, content='Muy buenas')
        message2 = Message.objects.create(user=self.user2, content='Hola')
        message3 = Message.objects.create(
            user=self.user3, content='Hola soy un espia')

        self.thread.messages.add(message1, message2, message3)

        self.assertEqual(self.thread.messages.all().count(), 2)

    def test_find_thread_with_custom_manager(self):
        self.thread.users.add(self.user1, self.user2)
        thread = Thread.objects.find(self.user1, self.user2)
        self.assertEqual(self.thread, thread)

    def test_find_or_create_thread_with_custom_manager(self):
        self.thread.users.add(self.user1, self.user2)
        thread = Thread.objects.find_or_create(self.user1, self.user3)
        self.assertIsNotNone(thread)
