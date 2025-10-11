"""
Duplicate Detection GUI
=======================

Graphical user interface for duplicate file detection using tkinter.

V2 Adapted from: trading-platform repository
Author: Agent-7 - Repository Cloning Specialist
Team Beta: Repo 6 Integration

Note: This is an optional component requiring tkinter. Graceful degradation
      is handled in __init__.py.
"""

import logging
import threading
import tkinter as tk
from pathlib import Path
from tkinter import filedialog, messagebox

from .dups_format import format_duplicates_text
from .file_hash import find_duplicate_files

logger = logging.getLogger(__name__)


def _format_duplicates_text(dups: dict[str, list[Path]]) -> str:
    """
    Backwards-compatible adapter for duplicate formatting.

    Args:
        dups: Dictionary mapping hash to list of duplicate paths

    Returns:
        Formatted text report
    """
    return format_duplicates_text(dups)


class DuplicateScannerGUI:
    def __init__(self) -> None:
        self.root = tk.Tk()
        self.root.title("Duplicate Scanner")
        self._build_menu()

        self.selected_path_var = tk.StringVar(value=str(Path.cwd()))

        path_frame = tk.Frame(self.root)
        path_frame.pack(fill=tk.X, padx=8, pady=8)

        tk.Label(path_frame, text="Folder:").pack(side=tk.LEFT)
        self.path_entry = tk.Entry(path_frame, textvariable=self.selected_path_var, width=60)
        self.path_entry.pack(side=tk.LEFT, padx=6, expand=True, fill=tk.X)
        self.browse_button = tk.Button(path_frame, text="Browse", command=self._on_browse)
        self.browse_button.pack(side=tk.LEFT)

        btn_frame = tk.Frame(self.root)
        btn_frame.pack(fill=tk.X, padx=8)
        self.scan_button = tk.Button(btn_frame, text="Scan", command=self._on_scan_clicked)
        self.scan_button.pack(side=tk.LEFT)
        self.clear_button = tk.Button(btn_frame, text="Clear", command=self._on_clear_clicked)
        self.clear_button.pack(side=tk.LEFT, padx=6)

        self.output = tk.Text(self.root, height=20, width=100)
        self.output.pack(fill=tk.BOTH, expand=True, padx=8, pady=8)

    def _on_browse(self) -> None:
        choice = filedialog.askdirectory(initialdir=self.selected_path_var.get() or str(Path.cwd()))
        if choice:
            self.selected_path_var.set(choice)

    def _on_clear_clicked(self) -> None:
        self.output.delete("1.0", tk.END)

    def _on_scan_clicked(self) -> None:
        """Handle scan button click event."""
        try:
            root = Path(self.selected_path_var.get()).resolve()
        except Exception as exc:  # pragma: no cover - GUI validation
            logger.error(f"Invalid path: {exc}")
            messagebox.showerror("Invalid path", str(exc))
            return

        if not root.exists() or not root.is_dir():  # pragma: no cover - GUI validation
            logger.warning(f"Path not found or not a directory: {root}")
            messagebox.showerror("Invalid path", f"Path not found or not a directory: {root}")
            return

        def work() -> None:
            self._scan_path(root)

        threading.Thread(target=work, daemon=True).start()

    def _scan_path(self, root: Path) -> None:
        """Scan the provided root directory and update the output text.

        Exposed for testability to enable synchronous execution in tests.
        """
        self._set_buttons_state(tk.DISABLED)
        try:
            files = [p for p in root.rglob("*") if p.is_file()]
            dups = find_duplicate_files(files)
            text = _format_duplicates_text(dups)
            self._set_output(text)
        finally:
            self._set_buttons_state(tk.NORMAL)

    def _set_output(self, text: str) -> None:
        self.output.delete("1.0", tk.END)
        self.output.insert(tk.END, text)

    def _set_buttons_state(self, state: str) -> None:
        """
        Set state of all buttons in the GUI.

        Args:
            state: tk state ('normal' or 'disabled')
        """
        for widget in self.root.winfo_children():
            for child in widget.winfo_children():
                if isinstance(child, tk.Button):
                    child.config(state=state)

    def _get_output_text(self) -> str:
        return self.output.get("1.0", tk.END)

    def _build_menu(self) -> None:
        menubar = tk.Menu(self.root)
        file_menu = tk.Menu(menubar, tearoff=0)
        file_menu.add_command(label="Save Report...", command=self._on_save_report_clicked)
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.root.quit)
        menubar.add_cascade(label="File", menu=file_menu)

        help_menu = tk.Menu(menubar, tearoff=0)
        help_menu.add_command(
            label="About",
            command=lambda: messagebox.showinfo(
                "About", "Duplicate Scanner\nFind duplicate files by content."
            ),
        )
        menubar.add_cascade(label="Help", menu=help_menu)

        self.root.config(menu=menubar)

    def _save_report(self, path: Path) -> None:
        text = self._get_output_text()
        # Normalize trailing newline like Text widget returns
        with path.open("w", encoding="utf-8") as f:
            f.write(text)

    def _on_save_report_clicked(self) -> None:  # pragma: no cover - UI dialog
        """Handle save report menu action."""
        filename = filedialog.asksaveasfilename(
            defaultextension=".txt",
            filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")],
            initialfile="duplicate_report.txt",
            title="Save Duplicate Report",
        )
        if filename:
            try:
                self._save_report(Path(filename))
                logger.info(f"Report saved to {filename}")
            except Exception as exc:
                logger.error(f"Save failed: {exc}")
                messagebox.showerror("Save failed", str(exc))

    def run(self) -> None:  # pragma: no cover - manual usage
        self.root.mainloop()


def main() -> int:  # pragma: no cover - manual usage
    app = DuplicateScannerGUI()
    app.run()
    return 0


if __name__ == "__main__":  # pragma: no cover
    raise SystemExit(main())
