from interactions import *
from bson import ObjectId

class Homework_remove(Extension):
    def __init__(self, bot, db):
        super().__init__()
        self.bot = bot
        self.db = db
        self.homework_db = db["homework"]

        self.setup_remove()
        self.setup_find()

    def setup_remove(self):
        @slash_command(
            name="removebyid",
            description="Permet de supprimer un devoir")
        @slash_option(
            name = "id",
            description= "Id du devoir à supprimer",
            required=True,
            opt_type=OptionType.STRING,
            )
        async def message_remove(ctx: SlashContext, id):
            self.homework_db.delete_one({"_id" : ObjectId(id)})
            await ctx.send(f"Devoir {id} supprimé")

        self.bot.add_command(message_remove)

    def setup_find(self):
        @slash_command(
            name="findhomeworkid",
            description="Permet de Trouver l'id un devoir")
        @slash_option(
            name = "nom",
            description= "Nom du devoir à trouver",
            required=True,
            opt_type=OptionType.STRING,
            )
        async def homework_find(ctx: SlashContext, nom):
            homework_id = self.homework_db.find_one({"name" : nom})["_id"]
            await ctx.send(f"l'id de {nom} est: {homework_id} \nutilise /removebyid {homework_id} pour le supprimer")


        self.bot.add_command(homework_find)