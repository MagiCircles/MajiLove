from math import ceil, floor

def calculateSongStat(song, card):
    color_bonus = 0.3 if card.photo.color == song.color else 0
    song_ids = [singer.id for singer in song.singers]
    singer_bonus = 0.1 if card.photo.cached_idol.id in song_ids else 0
    return card.base_stats * (1 + color_bonus + singer_bonus)

def photoToDict(song, photo):
    photoDict = {
        'dance' : photo.display_dance,
        'vocal' : photo.display_vocal,
        'charm' : photo.display_charm,
        'color' : photo.photo.color,
        'song_stat' : calculateSongStat(song, photo),
        'skill_type' : photo.photo.skill_type,
        'leader_skill_color' : photo.photo.leader_skill_color,
        'leader_skill_stat' : photo.photo.leader_skill_stat,
        'leader_skill_percentage': photo.final_leader_skill_percentage,
        'sub_skill_amount' : photo.sub_skill_amount,
    }
    for skill in ['cutin', 'perfect_score']:
        if photo.photo.skill_type == skill:
            photoDict[skill] = photo.skill_percentage
    for skill in ['score_notes', 'good_lock', 'great_lock', 'healer']
        if photo.photo.skill_type == skill:
            photoDict[skill] = photo.skill_note_count
    if photo.photo.sub_skill_type is 'full_combo':
        photoDict['full_combo_subskill'] = photo.sub_skill_amount
    elif photo.photo.sub_skill_percentage == 60:
        photoDict['stamina_60_subskill'] = photo.sub_skill_amount
    elif photo.photo.sub_skill_percentage == 80:
        photoDict['stamina_80_subskill'] = photo.sub_skill_amount
    return photoDict

def getLeaderSkillBonus(card, leader_color, leader_stat, leader_percent):
    if card['color'] == leader_color:
        return card['leader_stat'] * (leader_percent / 100)
    return 0

def estimatedSkillAutoStat(song, card):
    skill_added_stat = 0
    full_profile = 0.9 * song.difficulty_note_count
    if card['skill_type'] is 'score_notes':
        skill_added_stat = 2 * card['score_notes'] / song.difficulty_note_count
    elif card['skill_type'] is 'cutin':
        skill_added_stat = floor(song.difficulty_note_count / song.cut_in_freq) * (card['cutin'] / 100) / full_profile
    elif card['skill_type'] is 'healer':
        skill_added_stat = card['score_notes'] / song.difficulty_note_count
    elif card['skill_type'] is 'great_lock':
        skill_added_stat = 0.1 * card['score_notes'] / full_profile

    sub_skill_stat = card['sub_skill_amount'] / full_profile

    card['skill_added_stat'] = skill_added_stat
    card['sub_skill_added_stat'] = sub_skill_added_stat

    return card

# calculates score for a song given a play profile, team, and guest, team members have been processed with
def calculateScore(songProfile, leader, other_members, guest_color, guest_stat, guest_magnitude, event_stat):
    all_members = other_members.append(leader)
    team_stat = 0
    total_badgood = 0
    total_badgreat = 0
    total_scorenote = 0
    total_lifenote = 0
    total_perfectup = 0
    total_cutinbonus = 0
    full_combo_subskill = 0
    stamina_60_subskill = 0
    stamina_80_subskill = 0
    for member in all_members:
        team_stat += member['song_stat']
        if event_stat is not None:
            team_stat += member['event_stat']
        team_stat += getLeaderSkillBonus(member, guest_color, guest_stat, guest_magnitude)
        team_stat += getLeaderSkillBonus(member, leader['leader_skill_color'], leader['leader_skill_stat'], leader['leader_skill_percentage'])

        total_scorenote += member.get('score_notes', 0)
        total_perfectup += member.get('perfect_score', 0)
        total_cutinbonus += member.get('cutin', 0)
        total_badgood += member.get('good_lock', 0)
        total_badgreat += member.get('great_lock', 0)
        total_lifenote += member.get('healer', 0)

        full_combo_subskill += member.get('full_combo_subskill', 0)
        stamina_80_subskill += member.get('stamina_80_subskill', 0)
        stamina_60_subskill += member.get('stamina_60_subskill', 0)

    base_note_score = ceil(team_stat / 10)

    #Assume optimal order of notes for lockers

    bad_great_changed = min(songProfile.expected_bad, total_badgreat)
    good_great_changed = min(songProfile.expected_good, total_badgreat - bad_great_changed) if total_badgreat > bad_great_changed else 0
    bad_good_changed = min(songProfile.expected_bad - bad_great_changed, total_badgood)

    actual_miss = songProfile.expected_miss
    actual_bad = songProfile.expected_bad - bad_great_changed - bad_good_changed
    actual_good = songProfile.expected_good - good_great_changed + bad_good_changed
    actual_great = songProfile.expected_great + bad_great_changed + good_great_changed
    actual_perfect = songProfile.expected_perfect

    average_note = (actual_bad * 0.5 + actual_good * 0.9 + actual_great + actual_perfect * 1.1) / songProfile.difficulty_note_count

    full_combo = ((actual_miss + actual_bad) == 0)

    # this isn't actual accurate, but not sure what really happens
    stamina_lost = actual_bad * 3 + actual_miss * 5
    stamina_gained = total_lifenote * 5
    life_as_score_notes = max(0, floor((stamina_gained - stamina_lost) / 5))
    final_stamina = 100 - max(0, stamina_lost - stamina_gained)

    score_note_bonus = (life_as_score_notes + 2 * total_scorenote) * base_note_score * average_note
    cut_in_value = 2 * base_note_score * (1 + (total_cutinbonus / 100))
    # ignoring combo here for now
    cut_in_count = floor(songProfile.difficulty_note_count / songProfile.cut_in_freq)
    cut_in_bonus = cut_in_value * cut_in_count
    perfect_note_value = actual_perfect * round(round(1.1 * base_note_score) * (total_perfectup / 100))
    great_note_value = actual_great * base_note_score
    good_note_value = actual_good * round(0.9 * base_note_score)
    bad_note_value = actual_bad * round(0.5 * base_note_score)

    pre_final_score = perfect_note_value + great_note_value + good_note_value + bad_note_value + score_note_bonus + cut_in_bonus
    full_combo_bonus = 4 * base_note_score + full_combo_subskill if full_combo else 0
    stamina_60_bonus = stamina_60_subskill if final_stamina >= 60 else 0
    stamina_80_bonus = stamina_80_subskill if final_stamina >= 80 else 0
    return pre_final_score + full_combo_bonus + stamina_60_bonus + stamina_80_bonus

def calculateAutoScore(songProfile, leader, other_members, guest_color, guest_stat, guest_magnitude, event_stat):
    all_members = other_members.append(leader)
    team_stat = 0
    total_badgreat = 0
    total_scorenote = 0
    total_lifenote = 0
    total_cutinbonus = 0
    full_combo_subskill = 0
    stamina_60_subskill = 0
    stamina_80_subskill = 0
    for member in all_members:
        team_stat += member['song_stat']
        if event_stat is not None:
            team_stat += member['event_stat']
        team_stat += getLeaderSkillBonus(member, guest_color, guest_stat, guest_magnitude)
        team_stat += getLeaderSkillBonus(member, leader['leader_skill_color'], leader['leader_skill_stat'], leader['leader_skill_percentage'])
        total_scorenote += member.get('score_notes', 0)
        total_cutinbonus += member.get('cutin', 0)
        total_badgreat += member.get('great_lock', 0)
        total_lifenote += member.get('healer', 0)

        full_combo_subskill += member.get('full_combo_subskill', 0)
        stamina_60_subskill += member.get('stamina_60_subskill', 0)
        stamina_80_subskill += member.get('stamina_80_subskill', 0)

    base_note_score = ceil(team_stat / 10)

    #Assume optimal order of notes for lockers

    good_great_changed = min(songProfile.difficulty_note_count, total_badgreat)
    actual_good = songProfile.difficulty_note_count - good_great_changed
    actual_great = good_great_changed

    score_note_bonus = (total_lifenote + 2 * total_scorenote) * base_note_score * 0.9
    cut_in_value = 2 * base_note_score * (1 + (total_cutinbonus / 100))
    cut_in_count = floor(songProfile.difficulty_note_count / songProfile.cut_in_freq)
    cut_in_bonus = cut_in_value * cut_in_count

    pre_final_score = (actual_good * 0.9 + actual_great) * base_note_score + score_note_bonus + cut_in_bonus
    full_combo_bonus = 4 * base_note_score + full_combo_subskill
    return pre_final_score + full_combo_bonus + stamina_60_subskill + stamina_80_subskill

