'''
task runner, @see https://www.pyinvoke.org/
'''

import os
from invoke import task
from pathlib import Path

@task
def startdb(ctx):
    port = '2900'
    pw = os.getenv('REDISCLI_AUTH')
    path = Path.cwd() / Path("data/redis-2900.conf")
    text = path.read_text().replace('{{PORT}}', port).replace('{{PASSWORD}}', pw)

    path = Path.cwd() / Path("data/redis.conf")
    with path.open(mode='w', encoding='utf-8') as file:
        file.write(text)

    ctx.run('redis-server data/redis.conf')

@task
def stopdb(ctx):
    ctx.run('redis-cli -p 2900 shutdown')

@task
def run(ctx):
    ctx.run('/bin/rm -fr logs/*')
    ctx.run('poetry run bin/async-redis')

@task
def test(ctx):
    ctx.run('poetry run pytest --cov=async_redis/ --cov-branch tests/', pty=True)

@task(aliases=['cov'])
def cover(ctx):
    ctx.run('poetry run coverage report -m', pty=True)
    ctx.run('poetry run coverage html --title="Async Redis Test Coverage"', pty=True)

@task(aliases=['int'])
def integration(ctx):
    ctx.run('poetry run tests/integration-tests.py --insert', pty=True)

@task(name='format', aliases=['black','isort'])
def formatter(ctx):
    ctx.run('black async_redis/ tests/', pty=True)
    ctx.run('isort async_redis/', pty=True)
    ctx.run('poetry run ruff check --fix ./async_redis/', pty=True)

@task
def ruff(ctx):
    ctx.run('poetry run ruff check ./async_redis/', pty=True)

@task
def lint(ctx):
    ctx.run('poetry run ruff check ./async_redis/', pty=True)
    ctx.run('poetry run pylint ./async_redis/', pty=True)

@task(aliases=['todo'])
def todos(ctx):
    ctx.run('rg TODO async_redis/*.py tests/*.py', pty=True)

@task
def mypy(ctx):
    ctx.run('poetry run mypy async_redis/', pty=True)

@task
def refurb(ctx):
    ctx.run('poetry run refurb async_redis/ tests/', pty=True)

@task
def repl(ctx):
    ctx.run('poetry run bpython -i .repl-start.py', pty=True)

@task(aliases=['precommit'])
def pre(ctx):
    ctx.run('clear', pty=True)
    test(ctx)
    cover(ctx)
    formatter(ctx)
    lint(ctx)
    refurb(ctx)
    mypy(ctx)

