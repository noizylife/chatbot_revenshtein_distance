import pandas as pd


class SimpleChatBot:
    # 초기화 메서드
    def __init__(self, filepath):
        self.questions, self.answers = self.load_data(filepath)

    # Chat Data 불러오기 메서드
    def load_data(self, filepath):
        data = pd.read_csv(filepath)
        questions = data['Q'].tolist()  # 질문열만 뽑아 파이썬 리스트로 저장
        answers = data['A'].tolist()   # 답변열만 뽑아 파이썬 리스트로 저장
        return questions, answers

    # 가장 유사한 답을 찾는 메서드
    def find_best_answer(self, input_sentence):
        min_distance = float('inf')   # 최소거리를 inf값으로 초기화
        best_match_index = -1         # index 초기화. -1 == 유사한 질문 없음
        # self.questions에서 각 질문의 index와 내용을 불러옴.
        for i, question in enumerate(self.questions):
            # 거리를 구하기 위해 levenshtein_distance 함수의 return을 distance 변수에 저장
            distance = self.levenshtein_distance(
                input_sentence, question)    # 입력 문장과 질문열의 내용을 비교하기 위해 인수로 넘김
            if distance < min_distance:      # 만일 levenshtein_distance의 return이 min_distance보다 작다면
                min_distance = distance      # min_distance에 distance의 질문 내용을 저장하고
                best_match_index = i         # 가장 적절한 질문 인덱스를 질문 내용의 인덱스로 저장

        if best_match_index != -1:           # levenshtein_distance에서 유사한 질문을 찾아냈다면
            # 질문열과 동일한 인덱스에서 답변값을 return한다.
            return self.answers[best_match_index]

    # levenshtein algorithm
    def levenshtein_distance(self, str_1, str_2):  # 인수로 문장 2개 입력 받음
        m = len(str_1)   # m x n
        n = len(str_2)
        # list comprehension으로 2차원 배열 0으로 초기화
        distance = [[0] * (n + 1) for _ in range(m + 1)]
        for i in range(m + 1):  # 첫번째 열 initial value 입력
            distance[i][0] = i
        for j in range(n + 1):  # 첫번째 행 initial value 입력
            distance[0][j] = j
        for i in range(1, m + 1):   # levenshtein algorithm에 의해 표 채우기
            for j in range(1, n + 1):
                # 조건 표현식. 행과 열을 비교해서 비교부분이 동일하면 0
                cost = 0 if str_1[i - 1] == str_2[j - 1] else 1

                # 거리 구하기. 삽입, 삭제, 변경 중 가장 작은 값을 불러온다.
                distance[i][j] = min(distance[i - 1][j] + 1,           # 문자 제거: 위쪽에서 +1
                                     # 문자 삽입: 왼쪽에서 +1
                                     distance[i][j - 1] + 1,
                                     distance[i - 1][j - 1] + cost)    # 문자 변경: 대각선에서 +1, 동일한 경우 대각선 숫자 복사

        return distance[m][n]


# CSV 파일 경로를 지정하세요.
filepath = '/Users/cellbit/chatbot_exercise/chatbot/ChatbotData.csv'

# 간단한 챗봇 인스턴스를 생성합니다.
chatbot = SimpleChatBot(filepath)

# '종료'라는 단어가 입력될 때까지 챗봇과의 대화를 반복합니다.
while True:
    input_sentence = input('You: ')
    if input_sentence.lower() == '종료':
        break
    response = chatbot.find_best_answer(input_sentence)
    print('Chatbot:', response)
