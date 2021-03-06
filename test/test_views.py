import pytest
from django.urls import reverse
from travel import models as travel


@pytest.mark.django_db
class TestViews:

    def test_search(self, client, user):
        r = client.get(reverse('travel-search'))
        assert r.status_code == 200

        # search_advanced r'^advanced/$'
        r = client.get(reverse('travel-search-advanced'))
        assert r.status_code == 302

        client.force_login(user)
        r = client.get(reverse('travel-search-advanced') + '?search=us')
        assert r.status_code == 200

    def test_entities(self, country, continent, client, user):
        # by_locale r'^i/(?P<ref>\w+)/$'
        r = client.get(reverse('travel-by-locale', args=[country.type.abbr]))
        assert r.status_code == 200

        r = client.get(reverse('travel-by-locale', args=['XX']))
        assert r.status_code == 404

        # entity r'^i/(?P<ref>\w+)/(?P<code>\w+)(?:-(?P<aux>\w+))?/$'
        r = client.get(reverse('travel-entity', args=[
            continent.type.abbr,
            continent.code
        ]))
        assert r.status_code == 200

        # entity r'^i/(?P<ref>\w+)/(?P<code>\w+)(?:-(?P<aux>\w+))?/$'
        r = client.get(reverse('travel-entity', args=[
            'XX',
            'XX'
        ]))
        assert r.status_code == 404
        
        # entity_relationships r'^i/(?P<ref>\w+)/(?P<code>\w+)(?:-(?P<aux>\w+))?/(?P<rel>\w+)/$'
        url = reverse('travel-entity-relationships', args=[
            continent.type.abbr,
            continent.code,
            country.type.abbr,
        ])
        r = client.get(url)
        assert r.status_code == 200

    def test_logs(self, client, continent, user):
        client.force_login(user)
        
        # entity r'^i/(?P<ref>\w+)/(?P<code>\w+)(?:-(?P<aux>\w+))?/$'
        r = client.get(reverse('travel-entity', args=[
            continent.type.abbr,
            continent.code
        ]))
        assert r.status_code == 200

        r = client.post(reverse('travel-entity', args=[
            continent.type.abbr,
            continent.code
        ]), {'arrival': '2018-03-07'})
        assert r.status_code == 302

        log = travel.TravelLog.objects.latest()

        # r'^([^/]+)/log/(\d+)/$
        r = client.get(reverse('travel-log-entry', args=[
            user.username,
            log.id
        ]))
        assert r.status_code == 200

        r = client.post(reverse('travel-log-entry', args=[
            user.username,
            log.id
        ]), {'arrival': '2018-03-15'})
        assert r.status_code == 302
        
    def test_no_bucketlist(self, client, user):
        # bucket_list r'^buckets/(\d+)/$'
        r = client.get(reverse('travel-bucket', args=[0]))
        assert r.status_code == 404

        # bucket_list_for_user r'^buckets/(\d+)/([^/]+)/$'
        r = client.get(reverse('travel-bucket-for_user', args=[0, user.id]))
        assert r.status_code == 404

        # bucket_list_comparison r'^buckets/(\d+)/(.+)/$'
        r = client.get(reverse('travel-bucket-comparison', args=[0, 'foo/bar']))
        assert r.status_code == 404

    def test_bucketlist(self, client, user, bucketlist, user2):
        r = client.get(reverse('travel-buckets'))
        assert r.status_code == 200

        # bucket_list r'^buckets/(\d+)/$'
        r = client.get(reverse('travel-bucket', args=[bucketlist.id]))
        assert r.status_code == 200

        # bucket_list_for_user r'^buckets/(\d+)/(\w+)/$'
        r = client.get(reverse('travel-bucket-for_user', args=[bucketlist.id, user.username]))
        assert r.status_code == 200

        # bucket_list_comparison r'^buckets/(\d+)/(.+)/$'
        r = client.get(reverse('travel-bucket-comparison', args=[
            bucketlist.id,
            '/'.join([user.username, user2.username])
        ]))
        assert r.status_code == 200

    def test_add_co(self, client, admin_user, continent, country_type):
        r = client.get(reverse('travel-entity-add-co'))
        assert r.status_code == 302

        client.force_login(admin_user)
        r = client.get(reverse('travel-entity-add-co'))
        assert r.status_code == 200

        r = client.post(reverse('travel-entity-add-co'), {})
        assert r.status_code == 200

        data = {
            'name': 'New Country',
            'full_name': 'New Full Name',
            'code': 'XZ',
            'locality': 'locality',
            'tz': 'UTC',
            'flag_url': '',
            'lat_lon': 'not good',
            'continent': continent.id
        }
        r = client.post(reverse('travel-entity-add-co'), data)
        assert r.status_code == 200

        data['lat_lon'] = '12.34 56.78'
        r = client.post(reverse('travel-entity-add-co'), data)
        assert r.status_code == 302
        assert travel.TravelEntity.objects.country('XZ')


    def test_profiles(self, client, user):
        # all_profiles r'^profiles/$',
        r = client.get(reverse('travel-profiles'))
        assert r.status_code == 200
        
        # profile r'^profiles/([^/]+)/$'
        r = client.get(reverse('travel-profile', args=[user.username]))
        assert r.status_code == 200

        #log_entry r'^profiles/([^/]+)/log/(\d+)/$'
        r = client.get(reverse('travel-log-entry', args=[user.username, 0]))
        assert r.status_code == 404

    def test_languages(self, client):
        r = client.get(reverse('travel-languages'))
        assert r.status_code == 200

        # language r'^languages/(\d+)/$',
        r = client.get(reverse('travel-language', args=[0]))
        assert r.status_code == 404

    def test_add(self, client):
        # start_add_entity r'^add/$',
        r = client.get(reverse('travel-entity-start-add'))
        assert r.status_code == 302

        #'travel-entity-add-co', # add_entity_co r'^add/co/$',
        r = client.get(reverse('travel-entity-add-co'))
        assert r.status_code == 302

        #'travel-entity-add-by-co', # add_entity_by_co r'^add/co/(\w+)/(\w+)/$',
        r = client.get(reverse('travel-entity-add-by-co', args=[0, 0]))
        assert r.status_code == 302

    def test_edit(self, client):
        # entity_edit r'^edit/i/(\w+)/(\w+)(?:-(\w+))?/$'
        r = client.get(reverse('travel-entity-edit', args=['xx', 'XX']))
        assert r.status_code == 302

        #client.force_login(page.user)

    def test_misc_views(self, client):
        assert client.get(reverse('travel-plugs')).status_code == 200
        assert client.get(reverse('travel-flag-quiz')).status_code == 200



