import pandas as pd


# 감정 사전 읽어 오기
import config


def open_emotion_dictionary():
    df_emotion = pd.read_excel(config.EMO_DICT_PATH, index_col=0)
    return df_emotion


def analyzeEmotion(df_emotion, token_list, lem_list):
    emotions = {"기쁨": 0.0, "슬픔": 0.0, "분노": 0.0, "놀람": 0.0, "혐오": 0.0, "공포": 0.0}

    # 형태소 분석 단어 기준 감정 분석 수행
    for token in token_list:
        emotion_list, score_list = find_word(df_emotion, token)
        if -1 not in emotion_list:
            for idx in range(len(emotion_list)):
                emotions[emotion_list[idx]] += float(score_list[idx])

    # 원형 복원 단어 기준 감정 분석 수행
    for lem in lem_list:
        emotion_list, score_list = find_word_lemma(df_emotion, lem)
        if -1 not in emotion_list:
            for idx in range(len(emotion_list)):
                emotions[emotion_list[idx]] += float(score_list[idx])

    return emotions


# 감정 사전에서 단어(형태소) 검색 후 감정값 추출
def find_word(df_emotion, token):
    df_filter = df_emotion[((df_emotion['한글'] == token[0]) & (df_emotion['품사'] == token[1]))]
    if len(df_filter) == 0:
        return [-1], [0]
    else:
        return df_filter['감정'].tolist(), df_filter['점수'].tolist()


# 감정 사전에서 단어(동사 원형) 검색 후 감정값 추출
def find_word_lemma(df_emotion, lemma):
    df_filter = df_emotion[(df_emotion['lemma'] == lemma)]
    if len(df_filter) == 0:
        return [-1], [0]
    else:
        return df_filter['감정'].tolist(), df_filter['점수'].tolist()
