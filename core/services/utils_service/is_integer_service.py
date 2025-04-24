class IsIntegerService:
    async def execute(self, value) -> bool:
        return -2_147_483_648 <= value <= 2_147_483_647
