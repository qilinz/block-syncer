import json
from mastodon import Mastodon
from mastodon.errors import MastodonNotFoundError
import time

def load_account_config(config_file):
    with open(config_file, 'r') as file:
        config = json.load(file)
    return config

def get_logged_in_instances(config):
    mastodon_instances = []
    for domain, accounts in config.items():
        # Register app for the domain (if not already registered)
        client_id, client_secret = Mastodon.create_app(
            'block-syncer-app',
            api_base_url=domain,
        )

        for account in accounts:
            email = account['email']
            password = account['password']
            # Log in to each account on this domain
            mastodon = Mastodon(client_id=client_id, client_secret=client_secret, api_base_url=domain)
            token = mastodon.log_in(
                email,
                password,
            )
            mastodon = Mastodon(access_token=token, api_base_url=domain)
            mastodon_instances.append(mastodon)
    return mastodon_instances

def get_mastodon_domain(mastodon):
    url = mastodon.api_base_url
    domain = url.replace("https://", "")
    return domain

def get_user_with_domin(mastodon, user):
    user_name = user["acct"]
    domain = get_mastodon_domain(mastodon)
    if "@" not in user_name:
        user_name = f"{user_name}@{domain}"
    return user_name


def fetch_block_users(mastodon):
    # todo fetch all blocks. currently it can only be 80
    block_users = mastodon.blocks(limit=80)
    print(block_users)
    block_users_with_domain = []
    for user in block_users:
        full_user_name = get_user_with_domin(mastodon, user)
        block_users_with_domain.append(full_user_name)
    print(len(block_users_with_domain))
    return block_users_with_domain

def fetch_block_domains(mastodon):
    block_domains = mastodon.domain_blocks()
    return block_domains

def get_user_id(mastodon, user):
    search_result = mastodon.account_search(user, limit=1)
    if search_result:
        full_user_name = get_user_with_domin(mastodon, search_result[0])
        if full_user_name == user:
            return search_result[0]["id"]
    return None


def apply_block_users(user_block_set, target_mastodon):
    current_block_users = fetch_block_users(target_mastodon)
    users_to_block = user_block_set - set(current_block_users)

    if not users_to_block:
        print("No new users to block.")
    else:
        print(f"{len(users_to_block)} users to block")
        for user in users_to_block:
            user_id = get_user_id(target_mastodon, user)
            print(f"Blocking {user}...")
            print(target_mastodon.account_block(user_id))
            time.sleep(0.5)
            break


def apply_block_domains(domain_block_set, target_mastodon):
    current_block_domains = fetch_block_domains(target_mastodon)
    domains_to_block = domain_block_set - set(current_block_domains)
    if not domains_to_block:
        print(f"No new domains to block")
    else:
        print(f"{len(domains_to_block)} domains to block")
        for domain in domains_to_block:
            target_mastodon.domain_block(domain)

def sync_blocks(mastodons):
    block_users = set()
    block_domains = set()

    for mastodon in mastodons:
        # print(mastodon.me())
        current_block_users = fetch_block_users(mastodon)
        block_users.update(current_block_users)
        current_block_domains = fetch_block_domains(mastodon)
        block_domains.update(current_block_domains)
    # for mastodon in mastodons:
    #     print(f"Working on {mastodon.me().get('url')}")
    #     apply_block_domains(block_domains, mastodon)
    #     apply_block_users(block_users, mastodon)
    #     break

def main():
    accounts_config = load_account_config('config.json')
    mastodon_instances = get_logged_in_instances(accounts_config)
    sync_blocks(mastodon_instances)
    print("finished")

if __name__ == "__main__":
    main()