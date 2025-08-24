from src.services.coordinator import MessageQueueClient


def test_send_and_receive():
    queue = MessageQueueClient()
    queue.send("msg")
    assert queue.receive() == "msg"
    assert queue.receive() is None
