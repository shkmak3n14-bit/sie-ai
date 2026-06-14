"""Interactive CLI for S.I.E."""

from __future__ import annotations

import sys

from rich.console import Console
from rich.panel import Panel
from rich.prompt import Prompt

from sie.flow import is_closing_request
from sie.llm import generate_closing, generate_greeting, generate_reply
from sie.session import Session

console = Console()

EXIT_COMMANDS = {"exit", "quit", "終了", "q"}


def print_sie(message: str) -> None:
    console.print(
        Panel(
            message,
            title="[bold blue]S.I.E.（サイ）[/bold blue]",
            border_style="blue",
            padding=(1, 2),
        )
    )


def print_info(message: str) -> None:
    console.print(f"[dim]{message}[/dim]")


def run() -> None:
    console.print()
    console.print(
        "[bold]S.I.E.（サイ）[/bold] — Support Intelligence on Ego",
        justify="center",
    )
    console.print(
        "[dim]終了するには exit / quit / 終了 と入力してください。[/dim]",
        justify="center",
    )
    console.print()

    session = Session.create()

    try:
        greeting = generate_greeting(session)
        print_sie(greeting)
    except ValueError as exc:
        console.print(f"[red]エラー: {exc}[/red]")
        sys.exit(1)
    except Exception as exc:
        console.print(f"[red]接続エラー: {exc}[/red]")
        sys.exit(1)

    while True:
        try:
            user_input = Prompt.ask("[bold green]あなた[/bold green]")
        except (KeyboardInterrupt, EOFError):
            console.print()
            print_info("セッションを終了します…")
            try:
                closing = generate_closing(session)
                print_sie(closing)
            except Exception:
                print_sie(
                    "必要なときに、必要なだけでいい。あなたのペースでいこう。"
                    "また声をかけてほしい。"
                )
            break

        if user_input.strip().lower() in EXIT_COMMANDS or is_closing_request(user_input):
            try:
                closing = generate_closing(session)
                print_sie(closing)
            except Exception as exc:
                console.print(f"[red]エラー: {exc}[/red]")
                print_sie(
                    "1mmでも前に進みたくなったら…また声をかけてほしい。"
                    "あなたのペースでいこう。"
                )
            break

        try:
            reply = generate_reply(session, user_input)
            print_sie(reply)
        except ValueError as exc:
            console.print(f"[red]エラー: {exc}[/red]")
            sys.exit(1)
        except Exception as exc:
            console.print(f"[red]エラー: {exc}[/red]")


def main() -> None:
    run()


if __name__ == "__main__":
    main()
