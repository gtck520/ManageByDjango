# Generated by Django 2.2.3 on 2019-07-20 13:14

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('news', '0003_articles_snap_nums'),
    ]

    operations = [
        migrations.CreateModel(
            name='ArticlesMedia',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('belong', models.IntegerField(default=0, verbose_name='资源所属')),
                ('belongtype', models.IntegerField(choices=[(0, '文章'), (1, '经文')], default=0, verbose_name='所属类型')),
                ('name', models.CharField(default='未命名', max_length=50, verbose_name='资源名称')),
                ('filename', models.FileField(max_length=200, upload_to='articles/%Y/%m', verbose_name='文件资源')),
                ('sort', models.IntegerField(default=0, verbose_name='排序')),
                ('add_time', models.DateTimeField(default=datetime.datetime.now, verbose_name='添加时间')),
            ],
            options={
                'verbose_name': '资源',
                'verbose_name_plural': '资源',
            },
        ),
        migrations.AddField(
            model_name='articles',
            name='news_type',
            field=models.IntegerField(choices=[(0, '文本'), (1, '图文'), (2, '多图'), (3, '视频')], default=0, verbose_name='内容类型'),
        ),
    ]
