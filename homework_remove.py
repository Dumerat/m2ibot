from interactions import *
from bson import ObjectId
from datetime import *

class Homework_remove(Extension):
    def __init__(self, bot, db):
        super().__init__()
        self.bot = bot
        self.db = db
        self.homework_db = db["homework"]

        self.setup_removebyid()
        self.setup_find()

    def setup_removebyid(self):
        @slash_command(
            name="removebyid",
            description="Permet de supprimer un devoir")
        @slash_option(
            name = "id",
            description= "Id du devoir à supprimer",
            required=True,
            opt_type=OptionType.STRING,
            )
        async def removebyid(ctx: SlashContext, id):
            self.homework_db.delete_one({"_id" : ObjectId(id)})
            await ctx.send(f"Devoir {id} supprimé")

        self.bot.add_command(removebyid)

    def setup_find(self):
        @slash_command(
            name="findhomeworkid",
            description="Permet de Trouver l'id d'un devoir")
        @slash_option(
            name = "nom",
            description= "Nom du devoir à trouver",
            required=True,
            opt_type=OptionType.STRING,
            )
        async def homework_find(ctx: SlashContext, nom):
            homework_items = self.homework_db.find({"name": nom})
            
            count = self.homework_db.count_documents({"name": nom})
            
            if count == 0:
                await ctx.send(f"Aucun devoir trouvé avec le nom {nom}.")
            else:
                message = f"Devoirs trouvés avec le nom {nom}:\n"
                for homework in homework_items:
                    homework_id = homework["_id"]
                    start_date = homework.get("start_date", "Date non trouvée !")
                    start_dated = start_date.strftime("%d %m %Y")
                    message += f"L'ID du devoir est : {homework_id} crée le {start_dated}\n"
                
                message += f"\nUtilise /removebyid <ID> pour supprimer un devoir."
                await ctx.send(message)




        self.bot.add_command(homework_find)