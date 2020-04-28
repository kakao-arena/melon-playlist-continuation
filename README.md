# Melon Playlist Continuation - 베이스라인 코드
카카오 아레나 Melon Playlist Continuation 대회 참가자에게 제공되는 예제 코드입니다. 간단한 추천 모델과 평가 코드가 포함되어 있습니다. 이 예제 코드에서는 Mel-spectrogram을 제외한 데이터를 사용하므로, 데이터셋 중 arena\_mel\_{0~39}.tar 파일은 이 예제를 실행하기 위해 다운받을 필요가 없습니다. 다음 예제는 주어진 train.json을 **새로운 train.json 과 val.json 으로** 8:2 의 비율로 나누어 로컬에서 테스팅 하는 코드로, **아레나에 제출 시 여기서 나뉘어진 val.json을 사용하면 틀린 결과가 나오니 아레나에서 다운받은 val.json을 사용해서 정답을 생성하시길 바랍니다.**

## 데이터 분할

res 폴더 안에 아레나에서 다운받은 파일들이 들어있다고 가정합니다. 학습과 개발 데이터를 나누기 위해 아래와 같이 실행합니다.

```bash
$> python split_data.py run res/train.json
```

실행 후 다음과 같은 폴더 구조를 확인할 수 있습니다.
	
```bash
$> tree -d
.
├── arena_data
│   ├── answers
│   ├── orig
│   └── questions
└── res
```

- 주어진 train.json을 train/val 8:2로 나누며, 여기서 나뉘어진 val은 문제 파일인 questions/val.json과 답안 파일인 answers/val.json으로 나뉘게 되고, 전체의 80%에 해당하는 새로운 train은 orig/train.json 에 저장됩니다.

## 추천 결과 생성

본 리포지토리에는 두가지 간단한 추천 모델이 제공됩니다. 아래에 나오는 부분은 위에서 새로 만들어진 train / val 셋에 대해 추천 결과를 만드는 방법이므로, **아레나에 제출 시 `arena_data/questions/val.json` 이 아닌 `res/val.json` 을 사용해야 정확한 답을 얻을 수 있습니다**

- `most_popular.py` 는 주어진 전체 플레이리스트에서 가장 많이 등장한 곡과 태그를 모든 문제에 대해서 답안으로 내놓는 모델입니다. 결과는 아래와 같이 생성할 수 있습니다. 
	
	```bash
	$> python most_popular.py run \
		--train_fname=arena_data/orig/train.json \
		--question_fname=arena_data/questions/val.json 
	```
	
- `genre_most_popular.py` 는 주어지는 각 문제마다, 가장 많이 등장하는 장르에 대해 해당 장르에서 가장 빈번하게 등장하는 곡들을 답안으로 내놓는 모델입니다. 위의 모델보다 성능이 약간 향상된 것을 확인할 수 있습니다. 결과는 아래와 같이 생성할 수 있습니다. 
	
	```bash
	$> python genre_most_popular.py run \
		--song_meta_fname=res/song_meta.json \
		--train_fname=arena_data/orig/train.json \
		--question_fname=arena_data/questions/val.json 
	```
	

추천 결과는 `arena_data/results/results.json` 에 저장됩니다. 해당 `results.json` 파일과 소스코드를 각각 zip파일로 압축한 후에 아레나 홈페이지로 제출하시면 점수를 확인하실 수 있습니다. 


## 평가

아레나에 제출하기 전에 본인이 만든 문제 / 정답 세트로 점수를 알아볼 수 있습니다. 위에서 생성된 추천 결과는 아래 커맨드로 평가할 수 있습니다.
	
```bash
$> python evaluate.py evaluate \
	--gt_fname=arena_data/answers/val.json \
	--rec_fname=arena_data/results/results.json 
```

`questions/val.json`을 패러미터로 넣었던 위의 추천 결과 생성 스크립트와는 다르게, `answers/val.json`을 패러미터로 넣어야 함을 주의해 주세요. 
