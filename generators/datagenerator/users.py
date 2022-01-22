# Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
# SPDX-License-Identifier: MIT-0

import random
import datetime
import uuid
import json
import numpy as np
import gzip
import codecs
import bisect
from faker import Faker
from faker.providers import internet
from faker.providers import user_agent
from faker.providers import profile
from scipy.stats import truncnorm

# Setup Faker
fake = Faker()
fake.add_provider(internet)
fake.add_provider(user_agent)
fake.add_provider(profile)

# Normally distribute ages between 18 and 100 with a mean age of 32.
age_min = 18
age_max = 100
age_mean = 32
age_sd = 15

age_dist = truncnorm((age_min - age_mean) / age_sd, (age_max - age_mean) / age_sd, loc=age_mean, scale=age_sd)

# Persona combinations ordered from strongest affinity to latent interest.
category_preference_personas = [
    'barleywine_mead_sour', 'belgian_farmhouse-ale_stout',
    'blonde-ale_golden-ale_wheat', 'bock_cream-ale_pale-ale',
    'brett_seasonal_smoked-beer', 'brown-ale_stout_red-ale',
    'cider_fruit_barleywine', 'cream-ale_root-beer_fruit',
    'farmhouse-ale_sour_golden-ale', 'fruit_pilsner_brett',
    'golden-ale_ipa_root-beer', 'ipa_pale-ale_farmhouse-ale',
    'kolsch_kombucha_brown-ale', 'kombucha_wheat_cider',
    'lager_cider_ipa', 'mead_smoked-beer_porter',
    'pale-ale_lager_blonde-ale', 'pilsner_kolsch_lager',
    'porter_red-ale_strong-ale', 'red-ale_bock_mead',
    'root-beer_blonde-ale_seasonal', 'seasonal_barleywine_kombucha',
    'smoked-beer_strong-ale_bock', 'sour_brett_kolsch',
    'stout_porter_cream-ale', 'strong-ale_brown-ale_belgian',
    'wheat_belgian_pilsner'
]

discount_personas = [
  'discount_indifferent',  # does not care about discounts
  'all_discounts',  # likes discounts all the time
  'lower_priced_products'  # likes discounts on cheaper products
]

class UserPool:
  def __init__(self):
    self.users = []
    self.active = []
    self.last_id = 0
    self.file = ''

  def size(self):
    return len(self.users) + len(self.active)

  def active_users(self):
    return len(self.active)

  def grow_pool(self, num_users):
    for i in range(num_users):
      self.last_id += 1
      user = User(str(self.last_id))
      self.users.append(user)

  def user(self, select_active=False):
    if not self.users:
      self.grow_pool(1000)
      self.save(self.file)  # Cache the whole pool back to the file
    if select_active and self.active:
      user = random.choice(self.active)
    else:
      user = self.users.pop(random.randrange(len(self.users)))
      self.active.append(user)
    return user

  def save(self, file):
    all_users = []
    all_users.extend(self.users)
    all_users.extend(self.active)
    json_data = json.dumps(all_users, default=lambda x: x.__dict__)
    with gzip.open(file, 'wt', encoding='utf-8') as f:
      f.write(json_data)
      f.close()

  @classmethod
  def from_file(cls, filename):
    user_pool = cls()
    user_pool.file = filename
    with gzip.open(filename, 'rt', encoding='utf-8') as f:
      data = json.load(f)
      f.close()
    user_ids = []
    for saved_user in data:
      user = User.from_file(saved_user)
      bisect.insort(user_ids, int(user.id))
      user_pool.last_id = user_ids[len(user_ids) - 1]
      user_pool.users.append(user)
    return user_pool

  @classmethod
  def new_file(cls, filename, num_users):
    user_pool = cls()
    user_pool.file = filename
    user_pool.grow_pool(num_users)
    user_pool.save(filename)
    return user_pool

class User:
  def __init__(self, id_string=None):
    if(id_string is not None):
      self.id = id_string
    else:
      self.id = str(random.randint(1000000000, 99999999999))
    self.gender = random.choice(['M', 'F'])
    if self.gender == 'F':
        self.first_name = fake.first_name_female()
        self.last_name = fake.last_name_female()
    else:
        self.first_name = fake.first_name_male()
        self.last_name = fake.last_name_male()

    address_state = fake.state_abbr(include_territories=True)
    email_first = self.first_name.replace(' ', '').lower()
    email_last = self.last_name.replace(' ', '').lower()
    self.email = f'{email_first}.{email_last}@example.com'
    self.age = int(age_dist.rvs())
    self.name = f'{self.first_name} {self.last_name}'
    self.username = f'user{self.id}'
    # These are hard-coded from the AWS samples Retail Demo Store workshop
    self.persona = random.choice(category_preference_personas)
    self.discount_persona = random.choice(discount_personas)
    self.traits = {}

    ios_token = fake.ios_platform_token()
    ios_identifiers = ios_token.split(' ')
    android_token = fake.android_platform_token()
    android_identifiers = android_token.split(' ')

    self.platforms = {
      "ios": {
        "anonymous_id": str(fake.uuid4()),
        "advertising_id": str(fake.uuid4()),
        "user_agent": ios_token,
        "model": ios_identifiers[0],
        "version": ios_identifiers[4]
      },
      "android": {
        "anonymous_id": str(fake.uuid4()),
        "advertising_id": str(fake.uuid4()),
        "user_agent": android_token,
        "version": android_identifiers[1]
      },
      "web": {
        "anonymous_id": str(fake.uuid4()),
        "user_agent": fake.user_agent()
      }
    }

    self.addresses = [
      {
        'first_name': self.first_name,
        'last_name': self.last_name,
        'address1': fake.street_address(),
        'address2': '',
        'country': 'US',
        'city': fake.city(),
        'state': address_state,
        'zipcode': fake.postcode_in_state(state_abbr=address_state),
        'default': True
      }
    ]

  def set_traits(self, traits):
    if traits is not None:
      for (k,v) in traits.items():
        self.traits[k] = random.choice(v)

  def get_platform_data(self, platform):
    return self.platforms[platform]

  def toJson(self):
    return self.__repr__()

  def __repr__(self):
    return json.dumps(self.__dict__)

  @classmethod
  def from_file(cls, user_dict):
    user = cls()
    for (k,v) in user_dict.items():
      setattr(user,k, v)  # Danger, Will Robinson
    return user
