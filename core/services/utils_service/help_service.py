class HelpService:
    def execute(self, commands):
        commands_str = ""

        for obj in commands:
            if isinstance(obj, str):
                commands_str += f"{obj}"
            else:
                for command in obj:
                    commands_str += f"/{command[0]} - {command[1]}\n"

        return commands_str
