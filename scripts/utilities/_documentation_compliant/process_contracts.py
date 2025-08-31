#!/usr/bin/env python3
"""Process contract IDs listed in config/contracts/contract_input.txt.

Reads the contract_input.txt file and iterates through every contract ID.
This ensures consumers handle all entries rather than just a single line.
"""

from pathlib import Path
from typing import List

CONTRACT_FILE = Path("config/contracts/contract_input.txt")


def load_contract_ids(path: Path = CONTRACT_FILE) -> List[str]:
        """
        load_contract_ids
        
        Purpose: Automated function documentation
        """
    """Load all contract IDs from ``contract_input.txt``.

    Args:
        path: Optional path to the contract ID file.

    Returns:
        A list of contract ID strings with whitespace stripped.
    """
    with path.open("r", encoding="utf-8") as fh:
        return [line.strip() for line in fh if line.strip()]


def main() -> None:
    """Iterate through contract IDs and print them."""
    for contract_id in load_contract_ids():
        print(contract_id)


if __name__ == "__main__":
    main()

