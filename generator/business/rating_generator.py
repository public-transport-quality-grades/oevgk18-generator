from generator.injector import registry


def start():
    cli = registry['ui']
    cli.foo()
