from interactions import *
from datetime import datetime
from interactions.api.events import Component
import asyncio

class Dashboard(Extension):
    def __init__(self, bot, db):
        super().__init__()
        self.bot = bot
        self.db = db

#auto update dashboard function
    async def dashboard_update(self, bot, db):
        homework_db = db["homework"]
        dash_db = db["data"]
        all_value, cyber_value, dev_value = [], [], []

        current_date = datetime.now()
        homeworks = homework_db.find().sort("subject")
        #remplie les listes des bons devoirs (il faudra trier les dates)
        for homework in homeworks:
            if homework['end_date'] >= current_date:
                if homework["class"] == "All":
                    all_value.append(f"{homework['name']} -.- {homework['link']} -.- {homework['subject']} -.- {homework['end_date'].strftime('%d %m %Y')}")
                elif homework["class"] == "Cyber2":
                    cyber_value.append(f"{homework['name']} -.- {homework['link']} -.- {homework['subject']} -.- {homework['end_date'].strftime('%d %m %Y')}")
                elif homework["class"] == "Dev":
                    dev_value.append(f"{homework['name']} -.- {homework['link']} -.- {homework['subject']} -.- {homework['end_date'].strftime('%d %m %Y')}")

        dash_info = dash_db.find_one({"id":"dash"})
        channel = bot.get_channel(str(dash_info["channel_id"]))
        if channel:
            dashboard = Embed(
            title="DASHBOARD",
            description="pas de desc pour le moment",
            color=0x018992,
            fields=[
                EmbedField(
                    name="Devoirs commun:",
                    value="\n".join([f"- [{item.split('-.-')[0]}]({item.split('-.-')[1]}) de {item.split('-.-')[2]} pour le: {item.split('-.-')[3]}" for item in all_value]) if all_value else " ",
                    inline=False,
                ),
                EmbedField(
                    name="Devoirs cyber2:",
                    value="\n".join([f"- [{item.split('-.-')[0]}]({item.split('-.-')[1]}) de {item.split('-.-')[2]} pour le: {item.split('-.-')[3]}" for item in cyber_value]) if cyber_value else " ",
                    inline=False,
                ),
                EmbedField(
                    name="Devoirs dev:",
                    value="\n".join([f"- [{item.split('-.-')[0]}]({item.split('-.-')[1]}) de {item.split('-.-')[2]} pour le: {item.split('-.-')[3]}" for item in dev_value]) if dev_value else " ",
                    inline=False,
                ),
            ])
            dashboard.set_thumbnail(
                url=bot.user.avatar_url,
            ),
            dashboard.set_image(
                url="",
            ),
            dashboard.set_footer(
                text=f"by {bot.owner.global_name}",
                icon_url=bot.user.avatar_url,
            )
            dash = await channel.fetch_message(str(dash_info["message_id"]))
            self.dash = dash
            if dash:
                await dash.edit(embed=dashboard)
            else:
                new_dash = await channel.send(embed=dashboard)
                dash_db.update_one(
                    {"id":"dash"},
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
            case "force_update": #not created yet
                await self.dashboard_update(self.bot, self.db)
    
    @slash_command(
        name="movedash",
        description="Permet de définir le channel du dashboard (owner only)")
    @check(is_owner())
    @slash_default_member_permission(Permissions.MANAGE_CHANNELS)
    async def moveDash(self, ctx: SlashContext):
        try:
            self.db["data"].update_one(
                {"id":"dash"},
                {"$set": {"channel_id": ctx.channel_id}}
            )
            # self.dash.delete() peut êtte une autre fois
            msg = await ctx.send(f"Le Dashboard va maintenant utiliser ce salon")
            await asyncio.sleep(20)
            await msg.delete()
        except:
            await ctx.send("i don't know how but that doesn't work...")