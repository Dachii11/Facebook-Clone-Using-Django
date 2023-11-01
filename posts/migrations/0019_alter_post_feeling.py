# Generated by Django 4.2.2 on 2023-10-04 11:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0018_alter_post_tags'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='feeling',
            field=models.CharField(blank=True, choices=[('accomplished', 'accomplished'), ('aggravated', 'aggravated'), ('alive', 'alive'), ('alone', 'alone'), ('amazed', 'amazed'), ('amazing', 'amazing'), ('amused', 'amused'), ('angry', 'angry'), ('annoyed', 'annoyed'), ('anxious', 'anxious'), ('awesome', 'awesome'), ('awful', 'awful'), ('bad', 'bad'), ('beautiful', 'beautiful'), ('better', 'better'), ('blah', 'blah'), ('blessed', 'blessed'), ('bored', 'bored'), ('broken', 'broken'), ('chill', 'chill'), ('cold', 'cold'), ('comfortable', 'comfortable'), ('confident', 'confident'), ('confused', 'confused'), ('content', 'content'), ('cool', 'cool'), ('crappy', 'crappy'), ('crazy', 'crazy'), ('curios', 'curios'), ('depressed', 'depressed'), ('determined', 'determined'), ('disappointed', 'disappointed'), ('down', 'down'), ('drained', 'drained'), ('drunk', 'drunk'), ('ecstatic', 'ecstatic'), ('emotional', 'emotional'), ('energized', 'energized'), ('excited', 'excited'), ('fantastic', 'fantastic'), ('fat', 'fat'), ('free', 'free'), ('fresh', 'fresh'), ('frustrated', 'frustrated'), ('full', 'full'), ('funny', 'funny'), ('good', 'good'), ('grateful', 'grateful'), ('great', 'great'), ('guilty', 'guilty'), ('happy', 'happy'), ('heartbroken', 'heartbroken'), ('helpless', 'helpless'), ('hopeless', 'hopeless'), ('hopeful', 'hopeful'), ('hopeless', 'hopeless'), ('horrible', 'horrible'), ('hot', 'hot'), ('hungry', 'hungry'), ('horny', 'horny'), ('hurt', 'hurt'), ('impatient', 'impatient'), ('in love', 'in love'), ('incomplete', 'incomplete'), ('inspired', 'inspired'), ('irritated', 'irritated'), ('lazy', 'lazy'), ('lonely', 'lonely'), ('lost', 'lost'), ('loved', 'loved'), ('lovely', 'lovely'), ('lucky', 'lucky'), ('mad', 'mad'), ('meh', 'meh'), ('miserable', 'miserable'), ('motivated', 'motivated'), ('nervous', 'nervous'), ('nostalgic', 'nostalgic'), ('OK', 'OK'), ('old', 'old'), ('optimistic', 'optimistic'), ('overwhelmed', 'overwhelmed'), ('pained', 'pained'), ('pissed', 'pissed'), ('pissed off', 'pissed off'), ('positive', 'positive'), ('pretty', 'pretty'), ('proud', 'proud'), ('pumped', 'pumped'), ('ready', 'ready'), ('refreshed', 'refreshed'), ('relaxed', 'relaxed'), ('relieved', 'relieved'), ('rough', 'rough'), ('sad', 'sad'), ('safe', 'safe'), ('satisfied', 'satisfied'), ('scared', 'scared'), ('sexy', 'sexy'), ('shocked', 'shocked'), ('sick', 'sick'), ('silly', 'silly'), ('sleepy', 'sleepy'), ('sore', 'sore'), ('sorry', 'sorry'), ('special', 'special'), ('stressed', 'stressed'), ('strong', 'strong'), ('stupid', 'stupid'), ('super', 'super'), ('surprised', 'surprised'), ('terrible', 'terrible'), ('thankful', 'thankful'), ('tired', 'tired'), ('uncomfortable', 'uncomfortable'), ('upset', 'upset'), ('weak', 'weak'), ('weird', 'weird'), ('well', 'well'), ('wonderfull', 'wonderfull'), ('worried', 'worried')], max_length=40, null=True),
        ),
    ]
