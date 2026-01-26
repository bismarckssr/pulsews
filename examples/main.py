from pulsews import PulseEngine, PulseHandler, ActivateObject, PulseLocalState
from dataclasses import dataclass, field
import json
import logging
import asyncio


# region FUNCTIONS
async def set_turn(message, obj):
	# Alterna clear_to_send quando ricevi "turn"
	obj.clear_to_send = not obj.clear_to_send

	# Due to how playscopa.online works, when the first cards are dealt, there is no "start playing" message.
	# Instead it is assumed by default that when "turn: true" arrives you can play. And turn true arrives before the cards are dealt.
	while not (hasattr(obj, 'array_of_cards') and obj.array_of_cards):
		await asyncio.sleep(0.1)  # Periodic checks at 0.1 seconds of delay

	# Pop the last card
	current_card = obj.array_of_cards.pop()

	# Return JSON answer
	return json.dumps(
		{
			'type': 'move',
			'card': {
				'valore': current_card.get('valore'),
				'seme': current_card.get('seme'),
			},
		}
	)


# Handler for startingCards: saves received cards
def set_cards(message, obj):
	arr = message.get('arr', [])
	if arr:
		obj.array_of_cards = arr


# Handler for remove_table_cards_combosAvail: in case of combos select the first one available
async def remove_combos(message, obj):
	combos = message.get('combos', [])
	selected_combo = combos[0]
	return json.dumps({'type': 'combo_response', 'combo': selected_combo})


# endregion

# Parameters are "enforced" by Callable type definition on action parameter
handler1 = PulseHandler(
	activate_object=ActivateObject(path=['type'], value='ping'),
	action=lambda message, _: json.dumps({'type': 'pong'}),
)

handler2 = PulseHandler(
	activate_object=ActivateObject(path=['type'], value='welcome'),
	action=lambda message, _: json.dumps({'type': 'options'}),
)

handler3 = PulseHandler(
	activate_object=ActivateObject(path=['turn'], value=True), action=set_turn
)

handler4 = PulseHandler(
	activate_object=ActivateObject(path=['type'], value='startingCards'),
	action=set_cards,
)

handler5 = PulseHandler(
	activate_object=ActivateObject(
		path=['type'], value='remove_table_cards_combosAvail'
	),
	action=remove_combos,
)


@dataclass
class PlayScopaObject(PulseLocalState):
	array_of_cards: [] = field(default_factory=list)
	clear_to_send: bool = False


stresser = PulseEngine(
	websocket_server_url='wss://ws.playscopa.online/',
	number_of_clients=500,
	duration=60,
	list_of_message_handlers=[handler1, handler2, handler3, handler4, handler5],
	local_state_class=PlayScopaObject,
)


async def main():
	await stresser.run()


if __name__ == '__main__':
	# Logging configuration
	logger = logging.getLogger('pulsews')
	logger.setLevel(logging.WARNING)

	# Starting the loop
	logging.info('Starting loop')
	asyncio.run(main())
