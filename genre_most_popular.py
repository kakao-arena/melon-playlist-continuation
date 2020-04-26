# -*- coding: utf-8 -*-
from collections import Counter

import fire
from tqdm import tqdm

from arena_util import load_json
from arena_util import write_json
from arena_util import remove_seen
from arena_util import most_popular


class GenreMostPopular:
    def _song_mp_per_genre(self, song_meta, global_mp):
        res = {}

        for sid, song in song_meta.items():
            for genre in song['song_gn_gnr_basket']:
                res.setdefault(genre, []).append(sid)

        for genre, sids in res.items():
            res[genre] = Counter({k: global_mp.get(int(k), 0) for k in sids})
            res[genre] = [k for k, v in res[genre].most_common(200)]

        return res

    def _generate_answers(self, song_meta_json, train, questions):
        song_meta = {int(song["id"]): song for song in song_meta_json}
        song_mp_counter, song_mp = most_popular(train, "songs", 200)
        tag_mp_counter, tag_mp = most_popular(train, "tags", 100)
        song_mp_per_genre = self._song_mp_per_genre(song_meta, song_mp_counter)

        answers = []
        for q in tqdm(questions):
            genre_counter = Counter()

            for sid in q["songs"]:
                for genre in song_meta[sid]["song_gn_gnr_basket"]:
                    genre_counter.update({genre: 1})

            top_genre = genre_counter.most_common(1)

            if len(top_genre) != 0:
                cur_songs = song_mp_per_genre[top_genre[0][0]]
            else:
                cur_songs = song_mp

            answers.append({
                "id": q["id"],
                "songs": remove_seen(q["songs"], cur_songs)[:100],
                "tags": remove_seen(q["tags"], tag_mp)[:10]
            })

        return answers

    def run(self, song_meta_fname, train_fname, question_fname):
        print("Loading song meta...")
        song_meta_json = load_json(song_meta_fname)

        print("Loading train file...")
        train_data = load_json(train_fname)

        print("Loading question file...")
        questions = load_json(question_fname)

        print("Writing answers...")
        answers = self._generate_answers(song_meta_json, train_data, questions)
        write_json(answers, "results/results.json")


if __name__ == "__main__":
    fire.Fire(GenreMostPopular)
