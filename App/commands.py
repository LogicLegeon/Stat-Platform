# App/commands.py

import sys
import pytest
import click
from flask.cli import with_appcontext

from App.database import db
from App.controllers import create_user, get_all_users, get_all_users_json, initialize

def init_app(app):
    # ─── init‑db ────────────────────────────────────────────────
    @app.cli.command("init‑db", help="Drop all tables, recreate, and seed initial data")
    @with_appcontext
    def init_db():
        db.drop_all()
        db.create_all()
        initialize()
        click.echo("✅ Database initialized.")

    # ─── user commands ───────────────────────────────────────────
    user_cli = click.Group("user", help="Manage user accounts")

    @user_cli.command("create", help="flask user create <username> <password>")
    @click.argument("username")
    @click.argument("password")
    @with_appcontext
    def create_user_cmd(username, password):
        create_user(username, password)
        click.echo(f"✅ User '{username}' created.")

    @user_cli.command("list", help="flask user list [string|json]")
    @click.argument("output", default="string", 
                    type=click.Choice(["string", "json"], case_sensitive=False))
    @with_appcontext
    def list_user_cmd(output):
        if output.lower() == "json":
            click.echo(get_all_users_json())
        else:
            users = get_all_users()
            if not users:
                click.echo("No users found.")
            for u in users:
                click.echo(f"{u.id}\t{u.username}")

    app.cli.add_command(user_cli)

    # ─── test commands ───────────────────────────────────────────
    test_cli = click.Group("test", help="Run test suites")

    @test_cli.command("user", help="flask test user [unit|int|all]")
    @click.argument("type", default="all", 
                    type=click.Choice(["unit", "int", "all"], case_sensitive=False))
    def test_user(type):
        if type == "unit":
            sys.exit(pytest.main(["-k", "UserUnitTests"]))
        elif type == "int":
            sys.exit(pytest.main(["-k", "UserIntegrationTests"]))
        else:
            sys.exit(pytest.main(["-k", "App"]))

    app.cli.add_command(test_cli)
