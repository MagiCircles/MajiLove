# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings
import magi.utils


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('majilove', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Idol',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(help_text=b'in romaji', unique=True, max_length=100, verbose_name='Name')),
                ('japanese_name', models.CharField(unique=True, max_length=100, verbose_name='Name (Japanese)')),
                ('d_names', models.TextField(null=True, verbose_name='Name')),
                ('i_group', models.PositiveIntegerField(null=True, verbose_name='Group', choices=[(0, 'ST\u2606RISH'), (1, b'QUARTET NIGHT')])),
                ('cv_name', models.CharField(help_text=b'in romaji', max_length=100, null=True, verbose_name='Voice actor')),
                ('japanese_cv_name', models.CharField(max_length=100, null=True, verbose_name='Voice actor (Japanese)')),
                ('d_cv_names', models.TextField(null=True, verbose_name='Name')),
                ('description', models.TextField(max_length=1000, null=True, verbose_name='Description')),
                ('d_descriptions', models.TextField(null=True, verbose_name='Description')),
                ('height', models.PositiveIntegerField(help_text=b'in cm', null=True, verbose_name='Height')),
                ('weight', models.PositiveIntegerField(help_text=b'in kg (0 = ?)', null=True, verbose_name='Weight')),
                ('i_blood_type', models.PositiveIntegerField(null=True, verbose_name='Blood Type', choices=[(0, b'O'), (1, b'A'), (2, b'B'), (3, b'AB'), (4, b'?')])),
                ('birthday', models.DateField(null=True, verbose_name='Birthday')),
                ('i_astrological_sign', models.PositiveIntegerField(null=True, verbose_name='Astrological Sign', choices=[(0, 'Leo'), (1, 'Aries'), (2, 'Libra'), (3, 'Virgo'), (4, 'Scorpio'), (5, 'Capricorn'), (6, 'Pisces'), (7, 'Gemini'), (8, 'Cancer'), (9, 'Sagittarius'), (10, 'Aquarius'), (11, 'Taurus')])),
                ('instrument', models.CharField(max_length=100, null=True, verbose_name='Instrument')),
                ('d_instruments', models.TextField(null=True, verbose_name='Instrument')),
                ('hometown', models.CharField(max_length=100, null=True, verbose_name='Hometown')),
                ('d_hometowns', models.TextField(null=True, verbose_name='Hometown')),
                ('hobby', models.CharField(max_length=100, null=True, verbose_name='Hobby')),
                ('d_hobbys', models.TextField(null=True, verbose_name='Hobby')),
                ('color', models.CharField(help_text=b'Format: #XXXXXX', max_length=7, verbose_name=b'Color')),
                ('image', models.ImageField(upload_to=magi.utils.uploadItem(b'idol'), verbose_name='Image')),
                ('owner', models.ForeignKey(related_name='added_idols', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Photo',
            fields=[
                ('id', models.PositiveIntegerField(unique=True, serialize=False, verbose_name='Album ID', primary_key=True, db_index=True)),
                ('name', models.CharField(max_length=100, null=True, verbose_name='Name')),
                ('japanese_name', models.CharField(max_length=100, null=True, verbose_name='Name (Japanese)')),
                ('d_names', models.TextField(null=True, verbose_name='Name')),
                ('release_date', models.DateTimeField(null=True, verbose_name='Release date', db_index=True)),
                ('ww_release_date', models.DateTimeField(null=True, verbose_name='Release date (English version)')),
                ('i_rarity', models.PositiveIntegerField(db_index=True, verbose_name='Rarity', choices=[(0, b'N'), (1, b'R'), (2, b'SR'), (3, b'UR')])),
                ('i_attribute', models.PositiveIntegerField(db_index=True, verbose_name='Attribute', choices=[(0, 'Star'), (1, 'Shine'), (2, 'Dream')])),
                ('image', models.ImageField(upload_to=magi.utils.uploadItem(b'photo/icon'), null=True, verbose_name='Icon')),
                ('image_special_shot', models.ImageField(upload_to=magi.utils.uploadItem(b'photo/icon/specialshot'), null=True, verbose_name='Icon (Special shot)')),
                ('photo', models.ImageField(upload_to=magi.utils.uploadItem(b'photo'), verbose_name='Photo')),
                ('photo_special_shot', models.ImageField(upload_to=magi.utils.uploadItem(b'photo/specialshot'), null=True, verbose_name='Photo (Special shot)')),
                ('transparent', models.ImageField(upload_to=magi.utils.uploadItem(b'photo/transparent'), null=True, verbose_name='Transparent')),
                ('transparent_special_shot', models.ImageField(upload_to=magi.utils.uploadItem(b'photo/transparent/specialshot'), null=True, verbose_name='Transparent (Special shot)')),
                ('art', models.ImageField(upload_to=magi.utils.uploadItem(b'photo/poster'), null=True, verbose_name='Poster')),
                ('art_special_shot', models.ImageField(upload_to=magi.utils.uploadItem(b'photo/poster/specialshot'), null=True, verbose_name='Poster (Special shot)')),
                ('autograph', models.ImageField(upload_to=magi.utils.uploadItem(b'photo/autograph'), null=True, verbose_name='Autograph')),
                ('message_image', models.ImageField(upload_to=magi.utils.uploadItem(b'photo/message'), null=True, verbose_name='Message')),
                ('message', models.TextField(max_length=500, null=True, verbose_name='Message')),
                ('japanese_message', models.TextField(max_length=500, null=True, verbose_name='Message (Japanese)')),
                ('d_messages', models.TextField(null=True, verbose_name='Message')),
                ('dance_min', models.PositiveIntegerField(verbose_name='Dance (Minimum)')),
                ('dance_max', models.PositiveIntegerField(verbose_name='Dance (Single copy maximum)')),
                ('dance_max_copy_max', models.PositiveIntegerField(null=True, verbose_name='Dance (Maxed copy maximum)')),
                ('vocal_min', models.PositiveIntegerField(verbose_name='Vocal (Minimum)')),
                ('vocal_max', models.PositiveIntegerField(verbose_name='Vocal (Single copy maximum)')),
                ('vocal_max_copy_max', models.PositiveIntegerField(null=True, verbose_name='Vocal (Maxed copy maximum)')),
                ('charm_min', models.PositiveIntegerField(verbose_name='Charm (Minimum)')),
                ('charm_max', models.PositiveIntegerField(verbose_name='Charm (Single copy maximum)')),
                ('charm_max_copy_max', models.PositiveIntegerField(null=True, verbose_name='Charm (Maxed copy maximum)')),
                ('i_leader_stat', models.PositiveIntegerField(null=True, verbose_name='Leader Skill', choices=[(0, 'Dance'), (1, 'Vocal'), (2, 'Charm')])),
                ('leader_skill_percentage', models.PositiveIntegerField(null=True, verbose_name='Leader Skill %')),
                ('i_skill_type', models.PositiveIntegerField(db_index=True, null=True, verbose_name='Skill', choices=[(0, 'Score notes'), (1, 'Perfect score up'), (2, 'Cut-in'), (3, 'Good(WW)/Great(JP) lock'), (4, 'Great(WW)/Perfect(JP) lock'), (5, 'Healer')])),
                ('skill_note_count', models.PositiveIntegerField(null=True, verbose_name=b'Skill Note Count')),
                ('skill_percentage', models.FloatField(null=True, verbose_name=b'Skill %')),
                ('i_sub_skill_type', models.PositiveIntegerField(null=True, verbose_name='Sub skill', choices=[(0, 'Full combo'), (1, 'Stamina based')])),
                ('sub_skill_amount', models.PositiveIntegerField(null=True, verbose_name=b'Sub Skill Amount')),
                ('sub_skill_percentage', models.FloatField(null=True, verbose_name=b'Sub Skill %')),
                ('sub_skill_increment', models.PositiveIntegerField(null=True, verbose_name=b'Sub Skill Level Up Increment')),
                ('_cache_idol_last_update', models.DateTimeField(null=True)),
                ('_cache_j_idol', models.TextField(null=True)),
                ('_cache_dance_rank', models.PositiveIntegerField(null=True)),
                ('_cache_vocal_rank', models.PositiveIntegerField(null=True)),
                ('_cache_charm_rank', models.PositiveIntegerField(null=True)),
                ('_cache_total_rank', models.PositiveIntegerField(null=True)),
                ('idol', models.ForeignKey(related_name='photos', verbose_name='Idol', to='majilove.Idol')),
                ('owner', models.ForeignKey(related_name='added_photos', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
    ]
