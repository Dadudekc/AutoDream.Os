task: "Consult Thea Manager for strategic guidance and capture logs"

context:
  url: "https://chatgpt.com/g/g-67f437d96d7c81918b2dbc12f0423867-thea-manager?model=gpt-5-thinking"
  message_file: "messages/thea_consultation_message.md"

steps:
  - run: |
      python scripts/consult_thea.py \
        --mode auto \
        --browser default \
        --delay 3 \
        --message-file "${message_file}" \
        --screenshot-after
    expect:
      - "Browser opened with Thea URL."
      - "Message copied to clipboard"
      - "Automated interaction completed" # or manual mode note

artifacts:
  - path: "consultation_logs/"
    required: true
    description: "Log files and optional screenshots of the consultation"

fallbacks:
  - condition: "GUI automation failed"
    action: |
      python scripts/consult_thea.py --mode manual --message-file "${message_file}" --delay 4
