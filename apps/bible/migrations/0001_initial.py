# Generated by Django 2.2.2 on 2019-07-02 15:20

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Books',
            fields=[
                ('SN', models.AutoField(max_length=11, primary_key=True, serialize=False, verbose_name='序号')),
                ('KindSN', models.IntegerField(max_length=11, verbose_name='归类')),
                ('ChapterNumber', models.IntegerField(max_length=11, verbose_name='章节数')),
                ('NewOrOld', models.IntegerField(choices=[(0, '旧约'), (1, '新约')], default=0, max_length=2, verbose_name='新旧约')),
                ('PinYin', models.CharField(max_length=10, verbose_name='拼音索引')),
                ('ShortName', models.CharField(max_length=10, verbose_name='简称')),
                ('FullName', models.CharField(max_length=20, verbose_name='全称')),
            ],
            options={
                'verbose_name': '圣经卷名',
                'verbose_name_plural': '圣经卷名',
            },
        ),
        migrations.CreateModel(
            name='Contents',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ChapterSN', models.IntegerField(max_length=11, verbose_name='章')),
                ('VerseSN', models.IntegerField(max_length=11, verbose_name='节')),
                ('Lection', models.CharField(max_length=255, verbose_name='内容')),
                ('SoundBegin', models.DecimalField(decimal_places=3, max_digits=10, verbose_name='语音开始')),
                ('SoundEnd', models.DecimalField(decimal_places=3, max_digits=10, verbose_name='语音结束')),
                ('VolumeSN', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='bible.Books', verbose_name='卷名')),
            ],
            options={
                'verbose_name': '章节内容',
                'verbose_name_plural': '章节内容',
            },
        ),
    ]
