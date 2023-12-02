from interactions import *
from datetime import datetime
from interactions.api.events import Component

class Dashboard(Extension):
    def __init__(self, bot, db):
        super().__init__()
        self.bot = bot
        self.db = db

#auto update dashboard function
    async def dashboard_update(self, bot, db):
        homework_db = db["homework"]
        dash_db = db["dashboard"]
        all_value, cyber_value, dev_value = [], [], []

        current_date = datetime.now()
        homeworks = homework_db.find().sort("subject")
        #rempli les listes des bon devoirs (il faudra trier les dates)
        for homework in homeworks:
            if homework['end_date'] >= current_date:
                if homework["class"] == "all":
                    all_value.append(f"{homework['name']} -.- {homework['link']} -.- {homework['end_date'].strftime('%d %m %Y')}")
                elif homework["class"] == "cyber2":
                    cyber_value.append(f"{homework['name']} -.- {homework['link']} -.- {homework['end_date'].strftime('%d %m %Y')}")
                elif homework["class"] == "dev":
                    dev_value.append(f"{homework['name']} -.- {homework['link']} -.- {homework['end_date'].strftime('%d %m %Y')}")

        dash_info = dash_db.find_one({"id":"1"})
        channel = bot.get_channel(str(dash_info["channel_id"]))
        if channel:
            dashboard = Embed(
            title="DASHBOARD",
            description="feur-feur-feur",
            color=0x018992,
            fields=[
                EmbedField(
                    name="Devoirs commun:",
                    value="\n".join([f"- [{item.split('-.-')[0]}]({item.split('-.-')[1]}) pour le: {item.split('-.-')[2]}" for item in all_value]) if all_value else " ",
                    inline=False,
                ),
                EmbedField(
                    name="Devoirs cyber2:",
                    value="\n".join([f"- [{item.split('-.-')[0]}]({item.split('-.-')[1]}) pour le: {item.split('-.-')[2]}" for item in cyber_value]) if cyber_value else " ",
                    inline=False,
                ),
                EmbedField(
                    name="Devoirs dev:",
                    value="\n".join([f"- [{item.split('-.-')[0]}]({item.split('-.-')[1]}) pour le: {item.split('-.-')[2]}" for item in dev_value]) if dev_value else " ",
                    inline=False,
                ),
            ])
            dashboard.set_thumbnail(
                url=bot.user.avatar_url,
            ),
            dashboard.set_image(
                url="https://img.freepik.com/vecteurs-libre/vecteur-degrade-logo-colore-oiseau_343694-1365.jpg?w=740&t=st=1701211535~exp=1701212135~hmac=7ffc50bd025a728e9303b8d754474d20311ae9ed63213116b34a030fbf86e58c",
            ),
            dashboard.set_footer(
                text=f"by {bot.owner.global_name}",
                icon_url=bot.user.avatar_url,
            )
            dash = await channel.fetch_message(str(dash_info["message_id"]))
            if dash:
                await dash.edit(embed=dashboard)
            else:
                new_dash = await channel.send(embed=dashboard)
                dash_db.update_one(
                    {"id":"1"},
                    {"$set": {"message_id": new_dash.id}}
                )
        else:
            print('Channel not defined OR DOOMED !')

    #auto update dashboard call
    @Task.create(IntervalTrigger(minutes=5))
    async def update(self):
        await self.dashboard_update(self.bot, self.db)

    @listen()
    async def on_startup(self):
        await self.dashboard_update(self.bot, self.db) #update the dashboard at the start
        self.update.start() #start the auto update task
    
    @listen(Component)
    async def on_component(self, event: Component):
        ctx = event.ctx
        match ctx.custom_id:
            case "force_update":
                await self.dashboard_update(self.bot, self.db)