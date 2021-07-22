from typing import List

from molgenis.bbmri_eric._model import Node
from molgenis.bbmri_eric.errors import EricError, EricWarning, ErrorReport


class Printer:
    def __init__(self):
        self.indents = 0

    def indent(self):
        self.indents += 1

    def dedent(self):
        self.indents = max(0, self.indents - 1)

    def reset(self):
        self.indents = 0

    def print(self, value: str = None):
        if value:
            print(f"{'  ' * self.indents}{value}")
        else:
            print()

    def print_node_title(self, node: Node):
        title = f"🌍 Node {node.code}"
        border = "=" * (len(title) + 1)
        self.print()
        self.print(border)
        self.print(title)
        self.print(border)

    def print_error(self, error: EricError):
        message = str(error)
        if error.__cause__:
            message += f" - Cause: {str(error.__cause__)}"
        self.print(f"❌ {message}")

    def print_warning(self, warning: EricWarning):
        self.print(f"⚠️ {warning.message}")

    def print_warnings(self, warnings: List[EricWarning]):
        for warning in warnings:
            self.print_warning(warning)

    def print_summary(self, report: ErrorReport):
        self.print()
        self.print("=======")
        self.print("Summary")
        self.print("=======")

        for node in report.nodes:
            if node in report.errors:
                message = f"❌ Node {node.code} failed"
                if node in report.warnings:
                    message += f" with {len(report.warnings[node])} warnings"
            elif node in report.warnings:
                message = (
                    f"⚠️ Node {node.code} succeeded but with "
                    f"{len(report.warnings[node])} warnings "
                )
            else:
                message = f"✅ Node {node.code} finished successfully"
            self.print(message)
