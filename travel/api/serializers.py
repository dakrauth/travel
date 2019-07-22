from itertools import chain
from django.conf import settings
from rest_framework import serializers

from django.contrib.auth.models import User
from ..models import TravelLog, TravelEntity


class TravelLogSerializer(serializers.ModelSerializer):

    class Meta:
        model = TravelLog
        fields = '__all__'


class TravelEntitySerializer(serializers.ModelSerializer):
    type_abbr = serializers.ReadOnlyField(source='type.abbr')
    flag_svg = serializers.ImageField(source='flag.svg', allow_null=True)
    country_name = serializers.ReadOnlyField(source='country.name')
    country_code = serializers.ReadOnlyField(source='country.code')
    country_flag_emoji = serializers.ReadOnlyField(source='country.flag.emoji')
    country_flag_svg = serializers.ImageField(source='country.flag.svg', allow_null=True)

    class Meta:
        model = TravelEntity
        fields = (
            'id',
            'code',
            'name',
            'locality',
            'flag_svg',
            'country_name',
            'country_code',
            'country_flag_svg',
            'country_flag_emoji',
            'type_abbr'
        )


class TravelUserLogSerializer(serializers.ModelSerializer):
    logs = serializers.SerializerMethodField()
    entities = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ['logs', 'entities']

    def get_logs(self, obj):
        return TravelLogSerializer(
            TravelLog.objects.filter(user=obj),
            many=True
        ).data

    def get_entities(self, obj):
        return TravelEntitySerializer(
            TravelEntity.objects.filter(
                travellog__user=obj
            ).distinct().select_related('country', 'flag', 'country__flag', 'type'),
            many=True
        ).data


def logs_for_user(username):
    return {
        'logs': TravelLogSerializer(
            TravelLog.objects.filter(user__username=username),
            many=True
        ).data,
        'entities': TravelEntitySerializer(
            TravelEntity.objects.filter(
                travellog__user__username=username
            ).distinct().select_related('country', 'flag', 'country__flag', 'type'),
            many=True
        ).data
    }


FLAG_GROUPS = [
    ['AT', 'LV', 'PE', 'PF'], ['AX', 'FO', 'NO', 'IS'], ['XE', 'GE', 'XI', 'DK'],
    ['HR', 'SK', 'SI', 'RS'], ['RU', 'BG', 'LU', 'NL'], ['LT', 'BO', 'GH', 'ET'],
    ['XW', 'LK', 'BT', 'AL'], ['TD', 'RO', 'AD', 'MD'], ['GN', 'ML', 'SN', 'CM'],
    ['BF', 'MM', 'GH', 'GW'], ['ZW', 'UG', 'MU', 'CF'], ['JO', 'PS', 'SS', 'KW'],
    ['BE', 'DE', 'AM', 'TD'], ['VU', 'ZA', 'GY', 'ER'], ['CR', 'TH', 'CU', 'SR'],
    ['AU', 'NZ', 'TC', 'CK'], ['BH', 'QA', 'MT', 'NP'], ['AR', 'HN', 'SV', 'NI'],
    ['EG', 'YE', 'SY', 'IQ'], ['IR', 'TJ', 'HU', 'BG'], ['BW', 'GM', 'TZ', 'TT'],
    ['GR', 'UY', 'LR', 'MY'], ['CD', 'NA', 'KN', 'CG'], ['LA', 'NE', 'GL', 'BD'],
    ['NG', 'NF', 'LB', 'LS'], ['AZ', 'UZ', 'EH', 'KM'], ['PL', 'MC', 'ID', 'SG'],
    ['TN', 'TR', 'MA', 'MR'], ['DZ', 'MR', 'PK', 'TR'], ['FI', 'SE', 'DK', 'XE'],
    ['SC', 'MU', 'CF', 'KM'], ['DO', 'PA', 'MQ', 'BI'], ['AG', 'BB', 'BA', 'LC'],
    ['EC', 'CO', 'VE', 'AM'], ['HK', 'IM', 'KG', 'AL'], ['CI', 'IE', 'IT', 'IN'],
    ['BD', 'JP', 'PW', 'GL'], ['AS', 'MX', 'MD', 'ME'], ['AF', 'LY', 'KN', 'MW'],
    ['MH', 'NR', 'SB', 'CW'], ['BY', 'KZ', 'TM', 'IR'], ['CL', 'TO', 'TW', 'TG'],
    ['BJ', 'MG', 'OM', 'AE'], ['SL', 'UZ', 'RW', 'VC'], ['FM', 'AW', 'SO', 'TV'],
    ['GD', 'GP', 'DM', 'MV'], ['FJ', 'VG', 'AI', 'MS'], ['GQ', 'DJ', 'BS', 'PH'],
    ['AQ', 'CY', 'XK', 'MO'], ['LI', 'SM', 'VA', 'GI'], ['EE', 'GA', 'UA', 'SL'],
    ['AO', 'KE', 'SZ', 'ZM'], ['BZ', 'CV', 'SX', 'CZ'], ['FK', 'KY', 'BM', 'TV'],
    ['VN', 'CN', 'TW', 'KP'], ['SD', 'PS', 'JO', 'EH'], ['HT', 'LI', 'PT', 'MN'],
    ['PG', 'CX', 'CC', 'WS'], ['XS', 'XI', 'FI', 'XE'], ['JM', 'MK', 'ST', 'SC'],
    ['AO', 'MZ', 'SZ', 'KE'], ['BN', 'KH', 'TL', 'TK'], ['FR', 'IE', 'IT', 'CI'],
    ['GT', 'MX', 'PY', 'AR'], ['IO', 'KI', 'CK'],
]


class FlagEntitySerializer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField()

    class Meta:
        model = TravelEntity
        fields = ['name', 'code', 'image']

    def get_image(self, obj):
        return obj.flag.svg.url


def flag_data():
    return {
        'countries': FlagEntitySerializer(
            TravelEntity.objects.countries().filter(
                code__in={*chain(*FLAG_GROUPS)}
            ).select_related('flag'),
            many=True
        ).data,
        'groups': FLAG_GROUPS
    }
