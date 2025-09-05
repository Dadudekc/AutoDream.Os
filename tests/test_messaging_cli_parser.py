import pathlib
import sys
from unittest.mock import ANY, patch

import pytest

ROOT = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from src.services.messaging_cli import create_enhanced_parser, main


def test_overnight_flag_parsed():
    """Parser sets overnight flag when provided."""
    parser = create_enhanced_parser()
    args = parser.parse_args(["--overnight"])
    assert args.overnight is True


@patch("src.services.messaging_cli.handle_message_commands")
@patch("src.services.messaging_cli.handle_onboarding_commands")
@patch("src.services.messaging_cli.handle_contract_commands")
@patch("src.services.messaging_cli.handle_utility_commands")
@patch("src.services.messaging_cli.handle_overnight_commands")
def test_overnight_handler_precedence(overnight, utility, contract, onboarding, message):
    """Overnight commands are handled before other handlers."""
    overnight.return_value = True
    with patch.object(sys, "argv", ["prog", "--overnight"]):
        main()
    overnight.assert_called_once()
    utility.assert_not_called()
    contract.assert_not_called()
    onboarding.assert_not_called()
    message.assert_not_called()
