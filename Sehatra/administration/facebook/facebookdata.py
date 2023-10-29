#pip install facebook-business
#pip install pandas
# pip install google-analytics-data
from facebook_business.api import FacebookAdsApi
from facebook_business.adobjects.page import Page
import json
import datetime
import requests


#auth
def authentification():
    global AUTH
    with open('administration/facebook/auth.json', 'r') as file:
        auth = json.load(file)  
    AUTH=auth

AUTH=authentification()


#information générale actuelle
def pageInformationData():
    authentification()
    FacebookAdsApi.init(app_id=AUTH['app_id'], app_secret=AUTH['app_secret'], access_token=AUTH['access_token'])

    #page information
    fields = ['name','fan_count',Page.Field.followers_count]
    page = Page(AUTH['page_id'])
    page_info = page.api_get(fields=fields)

    return page_info

#total des partages
def get_total_partages():
    since = (datetime.datetime.now() - datetime.timedelta(days=28)).strftime('%Y-%m-%d')
    until = datetime.datetime.now().strftime('%Y-%m-%d')
    base_url = f"https://graph.facebook.com/v17.0/{AUTH['page_id']}/posts"
    params = {
        "fields": "shares.summary(true)",
        "since": since,
        "until": until,
        "access_token": AUTH['access_token']
    }

    response = requests.get(base_url, params=params)
    data = response.json()

    total_shares = 0
    for post in data['data']:
        if 'shares' in post:
            total_shares += post['shares']['count']

    return total_shares

#total des commentaires
def get_total_comments():
    since = (datetime.datetime.now() - datetime.timedelta(days=28)).strftime('%Y-%m-%d')
    until = datetime.datetime.now().strftime('%Y-%m-%d')
    url = f"https://graph.facebook.com/v17.0/{AUTH['page_id']}/posts"
    params = {
        "fields": "comments.summary(true)",
        "since": since,
        "until":until,
        "access_token": AUTH['access_token']
    }

    response = requests.get(url, params=params)
    data = response.json()

    total_comments = 0
    for post in data['data']:
        if 'comments' in post:
            total_comments += post['comments']['summary']['total_count']

    return total_comments


#reaction sur une poste 
def get_post_reaction(post_id):
    url = f"https://graph.facebook.com/v17.0/{post_id}"

    params = {
        'access_token': AUTH['access_token'],
        'fields': 'reactions.summary(true)'
    }

    response = requests.get(url, params=params)

    if response.status_code == 200:
        data = response.json()
        reaction_count = data['reactions']['summary']['total_count']
        return reaction_count
    else:
        print("Une erreur s'est produite lors de la requête.")


#total des réactions
def totalReaction():
    since = (datetime.datetime.now() - datetime.timedelta(days=28)).strftime('%Y-%m-%d')
    until = datetime.datetime.now().strftime('%Y-%m-%d')
    #url
    url = f"https://graph.facebook.com/v17.0/{AUTH['page_id']}/posts?&since={since}&until={until}" 

    #parametre
    params = {
        'access_token': AUTH['access_token']
    }

    response = requests.get(url, params=params)
    reactions=0
    if response.status_code == 200:
        data = response.json()
        for post in data['data']:
            reactions+=get_post_reaction(post['id'])

    else:
        print("Une erreur s'est produite lors de la requête.")

    return reactions



def page_actuality(since,until):
    url = f"https://graph.facebook.com/v17.0/{AUTH['page_id']}/insights"

    params = {
        'metric': 'page_content_activity_by_action_type_unique,page_content_activity,page_views_total',
        'access_token': AUTH['access_token'],
        'since': since,
        'until': until
    }

    response = requests.get(url, params=params)
    if response.status_code == 200:
        data = response.json()
        insights_data = {}
        if 'data' in data:
            for insight in data['data']:
                metric = insight['name']
                value = insight['values'][0]['value']
                insights_data[metric] = value
        return insights_data
    else:
        print("Une erreur s'est produite lors de la requête.")
        return {}


def get_total_photo_views():
    since = (datetime.datetime.now() - datetime.timedelta(days=28)).strftime('%Y-%m-%d')
    until = datetime.datetime.now().strftime('%Y-%m-%d')
    metric='page_consumptions_by_consumption_type'
    url_coverage = f"https://graph.facebook.com/{AUTH['page_id']}/insights?metric={metric}&since={since}&until={until}&access_token={AUTH['access_token']}"
    response_coverage = requests.get(url_coverage)
    data = response_coverage.json()
    total_photo_views = 0

    for metric_data in data['data']:
        if  metric_data['period']=='days_28':
            donnee = metric_data['values']
            break
    total_photo_views=donnee[len(donnee)-1]['value']['photo view']
    autre_clics=donnee[len(donnee)-1]['value']['other clicks']
    try:
        link_clics=donnee[len(donnee)-1]['value']['link clicks']

    except:
        link_clics=0

    data_element={
        'photo_view':total_photo_views,
        'autres_clics':autre_clics,
        'link_clics':link_clics
    }
    return data_element

#VUE D’ensemble de la page sur une intervalle de temps
def page_vue_ensemble(since,until):
    authentification()
    # since = (datetime.datetime.now() - datetime.timedelta(days=28)).strftime('%Y-%m-%d')
    # until = datetime.datetime.now().strftime('%Y-%m-%d')
    metric='page_posts_impressions_unique,page_post_engagements,page_fan_adds_unique,page_follows'
    url_coverage = f"https://graph.facebook.com/{AUTH['page_id']}/insights?metric={metric}&since={since}&until={until}&access_token={AUTH['access_token']}"
    response_coverage = requests.get(url_coverage)
    data_coverage = response_coverage.json()
    try:
        #couverture
        for metric_data in data_coverage['data']:
            if metric_data['name'] == 'page_posts_impressions_unique' and metric_data['period']=='days_28':
                coverage_data = metric_data['values']
                break
        
        coverage = coverage_data[27]['value']

        #interaction
        for metric_data in data_coverage['data']:
            if metric_data['name'] == 'page_post_engagements' and metric_data['period']=='days_28':
                interaction_data = metric_data['values']
                break
        interactions = interaction_data[27]['value']

        #nouveau j'aime

        for metric_data in data_coverage['data']:
            if metric_data['name'] == 'page_fan_adds_unique' and metric_data['period']=='days_28':
                new_likes = metric_data['values']
                break

        like = new_likes[27]['value']

        #followers
        for metric_data in data_coverage['data']:
            if metric_data['name'] == 'page_follows' and metric_data['period']=='days_28':
                new_followers = metric_data['values']
                break

        followers = new_followers[24]['value']-new_followers[0]['value']
        
        autre_data=get_total_photo_views()
        data_element={
            'couverture':coverage,
            'interaction':interactions,
            'like':like,
            'Followers':followers,
            'reactions':totalReaction(),
            'comments':get_total_comments(),
            'partages':get_total_partages(),
            'photo_view':autre_data['photo_view'],
            'autres_clics':autre_data['autres_clics'],
            'link_clics':autre_data['link_clics'],
            'page_content_activity_by_action_type_unique':page_actuality(since,until)['page_content_activity_by_action_type_unique']['page post'],
            'page_views_total':page_actuality(since,until)['page_views_total'],
            'page_content_activity':page_actuality(since,until)['page_content_activity']
        }
        return data_element
    except KeyError:
        print("Erreur : Données d'insights indisponibles.")
        return None


def get_post_insights(post_id):
    url = f"https://graph.facebook.com/v17.0/{post_id}/insights"

    params = {
        'metric': 'post_engaged_users,post_impressions,post_impressions_unique',
        'access_token': AUTH['access_token']
    }
    total_engagement = 0
    total_impressions = 0

    response = requests.get(url, params=params)
    if response.status_code == 200:
        data = response.json()
        insights_data = {}
        if 'data' in data:
            for insight in data['data']:
                metric = insight['name']
                value = insight['values'][0]['value']
                insights_data[metric] = value
                if metric=='post_engaged_users':
                    total_engagement=+value
                elif metric=='post_impressions':
                    total_impressions=+value
        if total_impressions > 0:
            engagement_rate = (total_engagement / total_impressions) * 100
        else:
            engagement_rate = 0
        return insights_data,engagement_rate
    else:
        print("Une erreur s'est produite lors de la requête.")
        return {}

def get_post_interactions(post_id):
    url = f"https://graph.facebook.com/v17.0/{post_id}/insights"

    # Paramètres
    #Impressions-Couverture
    params = {
        'metric': 'post_reactions_like_total,post_reactions_love_total,post_reactions_wow_total,post_reactions_haha_total,post_reactions_sorry_total,post_reactions_anger_total,post_clicks_by_type,post_video_views',
        'access_token': AUTH['access_token']
    }

    response = requests.get(url, params=params)
    if response.status_code == 200:
        data = response.json()
        insights_data = {}
        if 'data' in data:
            for insight in data['data']:
                metric = insight['name']
                value = insight['values'][0]['value']
                insights_data[metric] = value
        return insights_data
    else:
        print("Une erreur s'est produite lors de la requête.")
        return {}

def get_post_shares_comments(post_id):
    url = f"https://graph.facebook.com/v17.0/{post_id}"

    params = {
        'fields': 'shares,comments',
        'access_token': AUTH['access_token']
    }

    response = requests.get(url, params=params)
    if response.status_code == 200:
        data = response.json()
        shares = data.get('shares', {}).get('count', 0)
        comments = data.get('comments', {}).get('data', {})
        data_element={
            'share':shares,
            'nb_comments':len(comments)
        }
        return data_element

    return {'share':0,'nb_comments':0}

#contenu récent
def contenu_recent(since,until):
    #url
    url = f"https://graph.facebook.com/v17.0/{AUTH['page_id']}/posts?fields=id,message,created_time,full_picture&since={since}&until={until}" 

    #parametre
    params = {
        'access_token': AUTH['access_token']
    }

    response = requests.get(url, params=params)
    if response.status_code == 200:
        data = response.json()
        for metric_data in data['data']:
           metric_data['reactions']=get_post_reaction(metric_data['id'])
           metric_data['interaction']=get_post_interactions(metric_data['id'])
           metric_data['partage']=get_post_shares_comments(metric_data['id'])
           metric_data['engagement_public']=get_post_insights(metric_data['id'])
        
    else:
        print("Une erreur s'est produite lors de la requête.")

    return data

def AudienceParSexe(since, until):
    authentification()
    url = f"https://graph.facebook.com/{AUTH['page_id']}/insights"

    params = {
        'access_token': {AUTH['access_token']},
        'metric': 'page_fans_gender_age',
        'since': since,
        'until': until
    }

    response = requests.get(url, params=params)

    if response.status_code == 200:
        data = response.json()
        
        if 'data' in data and data['data'] and 'values' in data['data'][0] and data['data'][0]['values']:
            demographics_data = data['data'][0]['values'][0]['value']
            nb_jaime = pageInformationData()['fan_count']
            nb_masculin = 0
            nb_feminin = 0
            nb_autre = 0
            pourcentage_masculin = 0
            pourcentage_feminin = 0
            pourcentage_autre = 0

            # Masculin
            for key, value in demographics_data.items():
                if key.startswith("M"):
                    nb_masculin += value

            # Féminin
            for key, value in demographics_data.items():
                if key.startswith("F"):
                    nb_feminin += value

            nb_autre = nb_jaime - (nb_feminin + nb_masculin)

            pourcentage_masculin = (nb_masculin * 100) / nb_jaime
            pourcentage_feminin = (nb_feminin * 100) / nb_jaime
            pourcentage_autre = (nb_autre * 100) / nb_jaime
            data_element = {
                'masculin': pourcentage_masculin,
                'feminin': pourcentage_feminin,
                'autre': pourcentage_autre,
                'nb_masculin': nb_masculin,
                'nb_feminin': nb_feminin,
                'nb_autre': nb_autre,
                'm':format(pourcentage_masculin * 0.01,'.2f'),
                'f': format(pourcentage_feminin * 0.01,'.2f'),
                'u': format(pourcentage_autre * 0.01,'.2f')
            }
            return data_element
        else:
            print("Les données nécessaires ne sont pas disponibles.")
    else:
        print("Une erreur s'est produite lors de la requête.")


import requests

def AudienceParAgeEtSexe(since, until):
    url = f"https://graph.facebook.com/{AUTH['page_id']}/insights"

    params = {
        'access_token': AUTH['access_token'],
        'metric': 'page_fans_gender_age',
        'since': since,
        'until': until
    }

    response = requests.get(url, params=params)

    if response.status_code == 200:
        data = response.json()

        if 'data' in data and data['data'] and 'values' in data['data'][0] and data['data'][0]['values']:
            demographics_data = data['data'][0]['values'][0]['value']

            if demographics_data:
                demographics_data_sorted = {k: v for k, v in sorted(demographics_data.items(), key=lambda item: item[1], reverse=True)}

                return demographics_data_sorted
            else:
                print("Les données démographiques sont vides.")
        else:
            print("Les données nécessaires ne sont pas disponibles.")
    else:
        print("Une erreur s'est produite lors de la requête.")



def get_fans_demographics_city():
    #ville
    cities_url = f"https://graph.facebook.com/{AUTH['page_id']}/insights"
    cities_params = {
        'access_token': {AUTH['access_token']},
        'metric': 'page_fans_city'
    }

    cities_response = requests.get(cities_url, params=cities_params)

    if cities_response.status_code == 200:
        cities_data = cities_response.json()
        cities_demographics = cities_data['data'][0]['values'][0]['value']
        return cities_demographics

      
    else:
        print("Une erreur s'est produite lors de la requête pour les villes.")

def get_fans_demographics_country():
    countries_url = f"https://graph.facebook.com/{AUTH['page_id']}/insights"
    countries_params = {
        'access_token': {AUTH['access_token']},
        'metric': 'page_fans_country'
    }

    countries_response = requests.get(countries_url, params=countries_params)

    if countries_response.status_code == 200:
        countries_data = countries_response.json()
        countries_demographics = countries_data['data'][0]['values'][0]['value']
        return countries_demographics

    else:
        print("Une erreur s'est produite lors de la requête pour les pays.")
