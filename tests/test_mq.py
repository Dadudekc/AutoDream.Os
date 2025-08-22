import sys; sys.path.append("src"); import services.v1_v2_message_queue_system as mq; print("Module imported:", mq.__file__); print("Classes:", [x for x in dir(mq) if x[0].isupper()])
