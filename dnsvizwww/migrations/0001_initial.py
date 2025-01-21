# Generated by Django 5.1.5 on 2025-01-20 22:27

import django.core.validators
import django.db.models.deletion
import dnsviz.analysis.offline
import dnsvizwww.fields
import re
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='DNSServer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ip_address', models.GenericIPAddressField(unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='DomainName',
            fields=[
                ('name', dnsvizwww.fields.DomainNameField(max_length=2048, primary_key=True, serialize=False)),
                ('analysis_start', models.DateTimeField(blank=True, null=True)),
                ('refresh_interval', models.PositiveIntegerField(blank=True, null=True)),
                ('refresh_offset', models.PositiveIntegerField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='NSNameNegativeResponse',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', dnsvizwww.fields.DomainNameField(max_length=2048, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='ResourceRecord',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', dnsvizwww.fields.DomainNameField(max_length=2048)),
                ('rdtype', dnsvizwww.fields.UnsignedSmallIntegerField()),
                ('rdclass', dnsvizwww.fields.UnsignedSmallIntegerField()),
                ('rdata_wire', models.BinaryField()),
                ('rdata_name', dnsvizwww.fields.DomainNameField(blank=True, db_index=True, max_length=2048, null=True)),
                ('rdata_address', models.GenericIPAddressField(blank=True, db_index=True, null=True)),
            ],
            options={
                'unique_together': {('name', 'rdtype', 'rdclass', 'rdata_wire')},
            },
        ),
        migrations.CreateModel(
            name='DNSQueryOptions',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('flags', dnsvizwww.fields.UnsignedSmallIntegerField()),
                ('edns_max_udp_payload', dnsvizwww.fields.UnsignedSmallIntegerField(blank=True, null=True)),
                ('edns_flags', dnsvizwww.fields.UnsignedIntegerField(blank=True, null=True)),
                ('edns_options', models.BinaryField(blank=True, null=True)),
                ('tcp_first', models.BooleanField(default=False)),
            ],
            options={
                'unique_together': {('flags', 'edns_max_udp_payload', 'edns_flags', 'edns_options', 'tcp_first')},
            },
        ),
        migrations.CreateModel(
            name='DNSQuery',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('qname', dnsvizwww.fields.DomainNameField(max_length=2048)),
                ('rdtype', dnsvizwww.fields.UnsignedSmallIntegerField()),
                ('rdclass', dnsvizwww.fields.UnsignedSmallIntegerField()),
                ('response_options', dnsvizwww.fields.UnsignedSmallIntegerField(default=0)),
                ('version', models.PositiveSmallIntegerField(default=3)),
                ('options', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='queries', to='dnsvizwww.dnsqueryoptions')),
            ],
        ),
        migrations.CreateModel(
            name='DNSResponse',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('server', models.GenericIPAddressField()),
                ('client', models.GenericIPAddressField()),
                ('flags', dnsvizwww.fields.UnsignedSmallIntegerField(blank=True, null=True)),
                ('has_question', models.BooleanField(default=True)),
                ('question_name', dnsvizwww.fields.DomainNameField(blank=True, max_length=2048, null=True)),
                ('question_rdtype', dnsvizwww.fields.UnsignedSmallIntegerField(blank=True, null=True)),
                ('question_rdclass', dnsvizwww.fields.UnsignedSmallIntegerField(blank=True, null=True)),
                ('edns_max_udp_payload', dnsvizwww.fields.UnsignedSmallIntegerField(blank=True, null=True)),
                ('edns_flags', dnsvizwww.fields.UnsignedIntegerField(blank=True, null=True)),
                ('edns_options', models.BinaryField(blank=True, null=True)),
                ('error', models.PositiveSmallIntegerField(blank=True, null=True)),
                ('errno', models.PositiveSmallIntegerField(blank=True, null=True)),
                ('response_time', models.PositiveSmallIntegerField()),
                ('history_serialized', models.CharField(blank=True, max_length=4096, validators=[django.core.validators.RegexValidator(re.compile('^\\d+(?:,\\d+)*\\Z'), code='invalid', message='Enter only digits separated by commas.')])),
                ('msg_size', dnsvizwww.fields.UnsignedSmallIntegerField(blank=True, null=True)),
                ('query', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='responses', to='dnsvizwww.dnsquery')),
            ],
        ),
        migrations.CreateModel(
            name='NSMapping',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', dnsvizwww.fields.DomainNameField(max_length=2048)),
                ('server', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='dnsvizwww.dnsserver')),
            ],
            options={
                'unique_together': {('name', 'server')},
            },
        ),
        migrations.CreateModel(
            name='OnlineDomainNameAnalysis',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', dnsvizwww.fields.DomainNameField(max_length=2048)),
                ('stub', models.BooleanField(default=False)),
                ('analysis_type', dnsvizwww.fields.UnsignedSmallIntegerField(default=0)),
                ('explicit_delegation', models.BooleanField(default=False)),
                ('follow_ns', models.BooleanField(default=False)),
                ('follow_mx', models.BooleanField(default=False)),
                ('analysis_start', models.DateTimeField()),
                ('analysis_end', models.DateTimeField(db_index=True)),
                ('dep_analysis_end', models.DateTimeField()),
                ('version', models.PositiveSmallIntegerField(default=26)),
                ('parent_name_db', dnsvizwww.fields.DomainNameField(blank=True, max_length=2048, null=True)),
                ('dlv_parent_name_db', dnsvizwww.fields.DomainNameField(blank=True, max_length=2048, null=True)),
                ('nxdomain_ancestor_name_db', dnsvizwww.fields.DomainNameField(blank=True, max_length=2048, null=True)),
                ('referral_rdtype', dnsvizwww.fields.UnsignedSmallIntegerField(blank=True, null=True)),
                ('auth_rdtype', dnsvizwww.fields.UnsignedSmallIntegerField(blank=True, null=True)),
                ('cookie_rdtype', dnsvizwww.fields.UnsignedSmallIntegerField(blank=True, null=True)),
                ('nxdomain_name', dnsvizwww.fields.DomainNameField(blank=True, max_length=2048, null=True)),
                ('nxdomain_rdtype', dnsvizwww.fields.UnsignedSmallIntegerField(blank=True, null=True)),
                ('nxrrset_name', dnsvizwww.fields.DomainNameField(blank=True, max_length=2048, null=True)),
                ('nxrrset_rdtype', dnsvizwww.fields.UnsignedSmallIntegerField(blank=True, null=True)),
                ('auth_ns_ip_mapping_db', models.ManyToManyField(related_name='s+', to='dnsvizwww.nsmapping')),
                ('auth_ns_negative_response_db', models.ManyToManyField(related_name='s+', to='dnsvizwww.nsnamenegativeresponse')),
                ('group', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='dnsvizwww.onlinedomainnameanalysis')),
            ],
            options={
                'get_latest_by': 'analysis_end',
                'unique_together': {('name', 'analysis_end'), ('name', 'group')},
            },
            bases=(dnsviz.analysis.offline.OfflineDomainNameAnalysis, models.Model),
        ),
        migrations.AddField(
            model_name='dnsquery',
            name='analysis',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='queries_db', to='dnsvizwww.onlinedomainnameanalysis'),
        ),
        migrations.CreateModel(
            name='OfflineDomainNameAnalysis',
            fields=[
            ],
            options={
                'proxy': True,
                'indexes': [],
                'constraints': [],
            },
            bases=('dnsvizwww.onlinedomainnameanalysis',),
        ),
        migrations.CreateModel(
            name='ResourceRecordDNSKEYRelated',
            fields=[
                ('resourcerecord_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='dnsvizwww.resourcerecord')),
                ('algorithm', models.PositiveSmallIntegerField()),
                ('key_tag', dnsvizwww.fields.UnsignedSmallIntegerField(db_index=True)),
                ('expiration', models.DateTimeField(blank=True, null=True)),
                ('inception', models.DateTimeField(blank=True, null=True)),
            ],
            bases=('dnsvizwww.resourcerecord',),
        ),
        migrations.CreateModel(
            name='ResourceRecordWithAddressInRdata',
            fields=[
            ],
            options={
                'proxy': True,
                'indexes': [],
                'constraints': [],
            },
            bases=('dnsvizwww.resourcerecord',),
        ),
        migrations.CreateModel(
            name='ResourceRecordWithNameInRdata',
            fields=[
            ],
            options={
                'proxy': True,
                'indexes': [],
                'constraints': [],
            },
            bases=('dnsvizwww.resourcerecord',),
        ),
        migrations.CreateModel(
            name='ResourceRecordDNSKEY',
            fields=[
            ],
            options={
                'proxy': True,
                'indexes': [],
                'constraints': [],
            },
            bases=('dnsvizwww.resourcerecorddnskeyrelated',),
        ),
        migrations.CreateModel(
            name='ResourceRecordDS',
            fields=[
            ],
            options={
                'proxy': True,
                'indexes': [],
                'constraints': [],
            },
            bases=('dnsvizwww.resourcerecorddnskeyrelated',),
        ),
        migrations.CreateModel(
            name='ResourceRecordRRSIG',
            fields=[
            ],
            options={
                'proxy': True,
                'indexes': [],
                'constraints': [],
            },
            bases=('dnsvizwww.resourcerecorddnskeyrelated',),
        ),
        migrations.CreateModel(
            name='ResourceRecordA',
            fields=[
            ],
            options={
                'proxy': True,
                'indexes': [],
                'constraints': [],
            },
            bases=('dnsvizwww.resourcerecordwithaddressinrdata',),
        ),
        migrations.CreateModel(
            name='ResourceRecordMX',
            fields=[
            ],
            options={
                'proxy': True,
                'indexes': [],
                'constraints': [],
            },
            bases=('dnsvizwww.resourcerecordwithnameinrdata',),
        ),
        migrations.CreateModel(
            name='ResourceRecordNS',
            fields=[
            ],
            options={
                'proxy': True,
                'indexes': [],
                'constraints': [],
            },
            bases=('dnsvizwww.resourcerecordwithnameinrdata',),
        ),
        migrations.CreateModel(
            name='ResourceRecordSOA',
            fields=[
            ],
            options={
                'proxy': True,
                'indexes': [],
                'constraints': [],
            },
            bases=('dnsvizwww.resourcerecordwithnameinrdata',),
        ),
        migrations.CreateModel(
            name='ResourceRecordMapper',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('section', models.PositiveSmallIntegerField()),
                ('order', models.PositiveSmallIntegerField()),
                ('raw_name', dnsvizwww.fields.DomainNameField(blank=True, max_length=2048, null=True)),
                ('ttl', dnsvizwww.fields.UnsignedIntegerField()),
                ('message', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='rr_mappings', to='dnsvizwww.dnsresponse')),
                ('rdata', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='dnsvizwww.resourcerecord')),
            ],
            options={
                'unique_together': {('message', 'rdata', 'section')},
            },
        ),
    ]
