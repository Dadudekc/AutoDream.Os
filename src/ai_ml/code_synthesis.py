"""Code synthesis component for CodeCrafter.

This module turns a textual template into executable source code.  In the
original project this step delegated to large language models.  For the
purposes of the exercises in this kata we keep the synthesiser deterministic
and dependency free.
"""


class CodeSynthesizer:
    """Generate source code from a template string."""

    def synthesize_code(self, template: str) -> str:
        """Return a tiny Python function embedding the template text."""

        return (
            "def generated_function():\n"
            f"    \"\"\"{template}\"\"\"\n"
            "    return 'generated'\n"
        )

