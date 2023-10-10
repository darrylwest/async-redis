
project := "async_redis"

export PYTHONPATH := "async_redis/"

alias cov := cover
alias form := format
alias pre := precommit
alias todo := todos

# run the standard tests (default target)
test:
    /bin/rm -fr logs
    /bin/rm -fr data/test-*
    cp data/redis-template.conf data/test-template.conf
    poetry run pytest --cov=async_redis/ --cov-branch tests/

# run the standard tests + clippy and fmt
cover:
    poetry run coverage report -m
    poetry run coverage html --title="Redis Farm Test Coverage"

# invoke black, isort, ruff with --fix flag
format:
    black async_redis/ tests/
    isort async_redis/
    poetry run ruff check --fix ./async_redis/

# run ruff (no fix)
ruff:
    poetry run ruff check ./async_redis/

# ruff and pylint
lint:
    poetry run ruff check ./async_redis/
    poetry run pylint ./async_redis/

# dump the TODO hits
todos:
    rg TODO async_redis/*.py tests/*.py

# run mypy
mypy:
    poetry run mypy async_redis/

# runs refurb (slow)
refurb:
    poetry run refurb async_redis/ tests/

# watch src and test ; run tests on change
watch:
    watchexec -c -w async_redis/ -w tests/ -e .py -d 500 'just test lint'
    
# launch bpython and start with .repl-start.py script
repl:
    poetry run bpython -i .repl-start.py

# precommit tasks including test, cover, format, ruff, refurb and mypy
precommit:
    just test cover format lint refurb mypy

