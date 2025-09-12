from __future__ import annotations
def send_to_thea(message: str, *, username: str|None=None, password: str|None=None,
                 headless: bool=True, thread_url: str|None=None, resume_last: bool=False, attach_file: str|None=None):
    # Thin wrapper around your SimpleTheaCommunication module
    from simple_thea_communication import SimpleTheaCommunication
    thea = SimpleTheaCommunication(
        username=username, password=password, use_selenium=True,
        headless=headless, thread_url=thread_url, resume_last=resume_last, attach_file=attach_file
    )
    ok = thea.run_communication_cycle(message)
    thea.cleanup()
    return ok
