import json
from channels.generic.websocket import AsyncWebsocketConsumer
from .models import Quiz, Participant
from asgiref.sync import sync_to_async

class QuizConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.quiz_id = self.scope['url_route']['kwargs']['quiz_id']
        self.room_group_name = f'quiz_{self.quiz_id}'

        # Check if quiz exists
        try:
            self.quiz = await sync_to_async(Quiz.objects.get)(quiz_id=self.quiz_id)
        except Quiz.DoesNotExist:
            await self.close()
            return

        # Add user to the quiz participants
        self.user = self.scope["user"]
        self.participant, created = await sync_to_async(Participant.objects.get_or_create)(username=self.user.username, quiz=self.quiz)

        # Join room group
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        answer = text_data_json['answer']

        # Handle the answer submission
        await self.handle_answer_submission(answer)

    async def handle_answer_submission(self, answer):
        # Placeholder for actual answer checking and score updating logic
        correct = True  # Replace with actual checking logic
        if correct:
            self.participant.score += 1
            await sync_to_async(self.participant.save)()

        # Send updated score to group
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'score_update',
                'username': self.user.username,
                'score': self.participant.score,
            }
        )

        # Send updated leaderboard to group
        await self.send_leaderboard_update()

    async def score_update(self, event):
        username = event['username']
        score = event['score']

        # Send score update to WebSocket
        await self.send(text_data=json.dumps({
            'type': 'score_update',
            'username': username,
            'score': score,
        }))

    async def send_leaderboard_update(self):
        participants = await sync_to_async(list)(Participant.objects.filter(quiz=self.quiz).order_by('-score'))
        leaderboard = [
            {'username': participant.username, 'score': participant.score}
            for participant in participants
        ]

        # Send leaderboard update to group
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'leaderboard_update',
                'leaderboard': leaderboard,
            }
        )

    async def leaderboard_update(self, event):
        leaderboard = event['leaderboard']

        # Send leaderboard update to WebSocket
        await self.send(text_data=json.dumps({
            'type': 'leaderboard_update',
            'leaderboard': leaderboard,
        }))