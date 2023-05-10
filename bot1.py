import nextcord
from nextcord import Interaction
import requests
from bs4 import BeautifulSoup


client = nextcord.Client()

@client.event
async def on_ready():
        channel = client.get_channel(1072226424657813638)
        await channel.send('**Bots ir pie darba**')


@client.slash_command(name="run", description="Ieraksti Premier League komandu, atstarpes vietā ievieto `-`, visu raksti ar mazajiem burtiem!")
async def run(interaction: Interaction, komanda):
    channel = client.get_channel(1072226424657813638)
    komandas = ['arsenal', 'manchester-city', 'manchester-united',
                'newcastle-united','tottenham-hotspur', 'brighton-and-hove-albion', 
                'brentford', 'fulham', 'chelsea', 'liverpool','aston-villa', 
                'crystal-palace', 'nottingham-forest', 'leicester-city', 
                'wolverhampton-wanderers', 'west-ham-united', 'leeds-united', 
                'everton', 'bournemouth', 'southampton']

    if komanda == "arsenal":
        link = "https://upload.wikimedia.org/wikipedia/en/thumb/5/53/Arsenal_FC.svg/1200px-Arsenal_FC.svg.png"
    elif komanda == "manchester-city":
        link = "https://upload.wikimedia.org/wikipedia/en/thumb/e/eb/Manchester_City_FC_badge.svg/1200px-Manchester_City_FC_badge.svg.png"
    elif komanda == "manchester-united":
        link = "https://upload.wikimedia.org/wikipedia/en/thumb/7/7a/Manchester_United_FC_crest.svg/800px-Manchester_United_FC_crest.svg.png"
    elif komanda == "newcastle-united":
        link = "https://www.nufc.co.uk/media/28051/club-crest-1988-present.png?width=300&height=302"
    elif komanda == "tottenham-hotspur":
        link = "https://a.espncdn.com/combiner/i?img=/i/teamlogos/soccer/500/367.png"
    elif komanda == "brighton-and-hove-albion":
        link = "https://upload.wikimedia.org/wikipedia/en/thumb/f/fd/Brighton_%26_Hove_Albion_logo.svg/1200px-Brighton_%26_Hove_Albion_logo.svg.png"
    elif komanda == "brentford":
        link = "https://upload.wikimedia.org/wikipedia/en/thumb/2/2a/Brentford_FC_crest.svg/800px-Brentford_FC_crest.svg.png"
    elif komanda == "fulham":
        link = "https://s27807.pcdn.co/wp-content/uploads/Fulham-800x800.png"
    elif komanda == "chelsea":
        link = "https://upload.wikimedia.org/wikipedia/sco/thumb/c/cc/Chelsea_FC.svg/2048px-Chelsea_FC.svg.png"
    elif komanda == "liverpool":
        link = "https://upload.wikimedia.org/wikipedia/en/thumb/0/0c/Liverpool_FC.svg/1200px-Liverpool_FC.svg.png"
    elif komanda == "aston-villa":
        link = "https://upload.wikimedia.org/wikipedia/en/thumb/f/f9/Aston_Villa_FC_crest_%282016%29.svg/1200px-Aston_Villa_FC_crest_%282016%29.svg.png"
    elif komanda == "crystal-palace":
        link = "https://static.wikia.nocookie.net/logopedia/images/3/37/New_Crystal_Palace_FC_logo_%28January_choice_E%29.png/revision/latest/scale-to-width-down/250?cb=20120228203923"
    elif komanda == "nottingham-forest":
        link = "https://upload.wikimedia.org/wikipedia/sco/thumb/d/d2/Nottingham_Forest_logo.svg/1200px-Nottingham_Forest_logo.svg.png"
    elif komanda == "leicester-city":
        link = "https://upload.wikimedia.org/wikipedia/en/thumb/2/2d/Leicester_City_crest.svg/1200px-Leicester_City_crest.svg.png"
    elif komanda == "wolverhampton-wanderers":
        link = "https://logodownload.org/wp-content/uploads/2019/04/wolverhampton-logo-escudo.png"
    elif komanda == "west-ham-united":
        link = "https://upload.wikimedia.org/wikipedia/en/thumb/c/c2/West_Ham_United_FC_logo.svg/1200px-West_Ham_United_FC_logo.svg.png"
    elif komanda == "leeds-united":
        link = "https://upload.wikimedia.org/wikipedia/en/thumb/5/54/Leeds_United_F.C._logo.svg/1200px-Leeds_United_F.C._logo.svg.png"
    elif komanda == "everton":
        link = "https://assets.stickpng.com/images/580b57fcd9996e24bc43c4e3.png"
    elif komanda == "bournemouth":
        link = "https://upload.wikimedia.org/wikipedia/en/thumb/e/e5/AFC_Bournemouth_%282013%29.svg/1200px-AFC_Bournemouth_%282013%29.svg.png"
    elif komanda == "southampton":
        link = "https://upload.wikimedia.org/wikipedia/en/thumb/c/c9/FC_Southampton.svg/1200px-FC_Southampton.svg.png"


    if komanda in komandas:
        counter = 0

        url = f"https://www.skysports.com/{komanda}"

        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')

        table = soup.find('a', class_="standing-table__cell--name-link")
        games = soup.find_all('ul', class_='matches__group')
        lol = soup.find('tf', class_="standing-table__cell")

        for game in games:
            home_team = game.find('span', class_='matches__item-col matches__participant matches__participant--side1').text.strip()
            away_team = game.find('span', class_='matches__item-col matches__participant matches__participant--side2').text.strip()
            score = game.find('span', class_='matches__teamscores').text
            scorr = game.find_all("span", class_='matches__teamscores-side')
            league = game.find('span', class_="matches__item-col matches__label").text
            if "in play" not in score:
                print("Working")
            else:
                break


            for a in scorr:
                counter += 1
                if counter == 1:
                    embedTeam = home_team
                    embedInline = True
                    embed = nextcord.Embed(title=f"Komandas `{komanda}` pēdējās spēles.", description=f"{league.strip()} league")
                elif counter == 2:
                    embedTeam = away_team
                    embedInline = True
                    embed.add_field(name="VS", value="score", inline=True)
                elif counter == 3:
                    embedTeam = home_team
                    embedInline = True
                    embed.add_field(name="--------------------------------------------", value=f"{league.strip()} league", inline=False)
                elif counter == 4:
                    embedTeam = away_team
                    embedInline = True
                    embed.add_field(name="VS", value="score", inline=True)
                elif counter == 5:
                    embedTeam = home_team
                    embedInline = True
                    embed.add_field(name="--------------------------------------------", value=f"{league.strip()} league", inline=False)
                elif counter == 6:
                    embedTeam = away_team
                    embedInline = True
                    embed.add_field(name="VS", value="score", inline=True)
                elif counter == 7:
                    embedTeam = home_team
                    embedInline = True
                    embed.add_field(name="--------------------------------------------", value=f"{league.strip()} league", inline=False)
                elif counter == 8:
                    embedTeam = away_team
                    embedInline = True
                    embed.add_field(name="VS", value="score", inline=True)
                    

                embed.add_field(name=f"{embedTeam}", value=f"{a.text.strip()}", inline=embedInline)
    else:
        embedFail = nextcord.Embed(title=f"Komanda `{komanda}` netika atrasta.", description="Mēģiniet velreiz!\nAtstarpes vietā ievietojiet `-`\nVisu rakstiet ar mazajiem burtiem")
        await interaction.response.send_message(embed = embedFail)
    embed.set_thumbnail(url=link)
    await interaction.response.send_message(embed = embed)

client.run("MTA2OTY5ODkxNTM4Mjg1MzczMw.GEXwuE.vyihcHy5kX-rdfOCy3CVW6ovQGL_Vl0SSleeA4")