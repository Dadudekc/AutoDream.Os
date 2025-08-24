"""Validation routines for generated code."""


class CodeValidator:
    """Perform minimal validation on generated source code."""

    def validate(self, code: str) -> None:
        """Ensure the generated code looks plausible.

        The checks are intentionally lightweight: at the moment we only verify
        that the code contains at least one function definition.  Additional
        rules can be added without touching the orchestrating engine.
        """

        if "def " not in code:
            raise ValueError("Generated code must contain a function definition")

