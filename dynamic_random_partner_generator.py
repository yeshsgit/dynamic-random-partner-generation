import secrets
import hashlib
import uuid
import yaml


class Player:
    def __init__(self, name):
        self.name = name
        randomised_name_string = f"{self.name}{secrets.token_bytes(10)}{uuid.uuid4()}"
        encoded_randomised_name_string = randomised_name_string.encode(encoding='utf-8')
        random_hash_object = hashlib.sha256(string=encoded_randomised_name_string, usedforsecurity=True)
        self.id = random_hash_object.hexdigest()


def ultimate_shuffler(player_ids: list, iterations: int) -> list:
    length = len(player_ids)
    for i in range(iterations):
        pos_1 = secrets.randbelow(length)
        pos_2 = secrets.randbelow(length)
        player_ids[pos_1], player_ids[pos_2] = player_ids[pos_2], player_ids[pos_1]
    return player_ids

def select_pairs(player_ids: list) -> list[tuple[int, int]]:
    pairs = []
    player_ids_copy = player_ids.copy()
    length = len(player_ids)

    while length >= 2:
        pos_1 = secrets.randbelow(len(player_ids_copy))
        pos_2 = secrets.randbelow(len(player_ids_copy))
        if pos_1 != pos_2:
            pairs.append([player_ids_copy[pos_1], player_ids_copy[pos_2]])

            higher_pos = max(pos_1, pos_2)
            lower_pos = min(pos_1, pos_2)

            player_ids_copy.pop(higher_pos)
            player_ids_copy.pop(lower_pos)
            length = length - 2

    if len(player_ids_copy) == 1:
        pairs.append([player_ids_copy[0], "None"])

    return pairs


def main():
    with open(file="config.yaml", mode="rb") as config:
        config = yaml.safe_load(config)

    players = [Player(name.strip()) for name in config['players']]
    if len(players) < 2:
        raise ValueError("Atleast 2 player must be provided for the DRPG algorithm.")

    player_dict = {player.id : player.name for player in players}
    player_ids = list(player_dict.keys())
    players = [player_dict[player_id] for player_id in player_ids]
    # print(players)

    player_ids = ultimate_shuffler(player_ids=player_ids, iterations=1000)
    players = [player_dict[player_id] for player_id in player_ids]
    # print(players)

    pairs = select_pairs(player_ids=player_ids)
    player_pairs = [[player_dict[player_id] if player_id in player_ids else player_id for player_id in pair] for pair in pairs]
    print(player_pairs)




    
    


if __name__ == '__main__':
    main()