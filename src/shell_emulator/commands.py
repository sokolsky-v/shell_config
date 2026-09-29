class UnknownCommandError(Exception):
    pass


def run_ls_stub(arguments):
    return f"CMD: ls ARGS: {list(arguments)}"


def run_cd_stub(arguments):
    return f"CMD: cd ARGS: {list(arguments)}"


STUB_COMMAND_TABLE = {
    "ls": run_ls_stub,
    "cd": run_cd_stub,
}


def execute_stub_command(command_name, arguments):
    handler = STUB_COMMAND_TABLE.get(command_name)
    if handler is None:
        raise UnknownCommandError(command_name)
    return handler(arguments)