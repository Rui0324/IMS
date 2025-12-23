import os
from pathlib import Path

from rest_framework import permissions, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response


class AIViewSet(viewsets.ViewSet):
    permission_classes = [permissions.IsAuthenticated]

    @action(detail=False, methods=['post'])
    def recommend(self, request):
        payload = request.data.get('profile', '')
        recommendations = [
            {
                'title': 'AI 创业方向',
                'desc': '结合校园数据与兴趣，建议探索智能助教、校园能源优化等项目。',
            },
            {
                'title': '开源贡献',
                'desc': '参与学校开源社区，积累项目经验并提升履历。',
            },
        ]
        return Response({'input': payload, 'recommendations': recommendations})

    @action(detail=False, methods=['post'])
    def qa(self, request):
        question = request.data.get('question', '')
        answer = self._search_knowledge(question)
        return Response({'question': question, 'answer': answer})

    def _search_knowledge(self, question: str):
        base = Path(__file__).resolve().parents[2] / 'data' / 'knowledge'
        texts = []
        for path in base.glob('*.txt'):
            try:
                texts.append(path.read_text())
            except Exception:
                continue
        if not os.getenv('OPENAI_API_KEY'):
            return f"[mock] 根据知识库返回的回答：{question} 的参考建议。"
        if texts:
            return texts[0][:200]
        return 'No knowledge available.'
