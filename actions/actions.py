from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import SlotSet

class ActionValidarSabor(Action):
    """Valida se o sabor é feito pela pizzaria"""

    def name(self) -> Text:
        return "action_validar_sabor"
    
    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        sabor = tracker.get_slot("sabor")

        sabores_disponiveis = ["portuguesa", "calabresa", "frango", "mussarela", "margherita", "picanha"]

        if sabor and sabor.lower() in sabores_disponiveis:
            dispatcher.utter_message(text=f"Boa escolha! Pizza de {sabor} é nossa especialidade.")
            return []
        else:
            dispatcher.utter_message(text=f"Não temos pizza de {sabor}, escolha outro sabor.")
            return [SlotSet("sabor", None)]


class ActionValidarTamanho(Action):
    """Valida se o tamanho informado é suportado pela pizzaria."""

    def name(self) -> Text:
        return "action_validar_tamanho"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        tamanho = tracker.get_slot("tamanho")
        validos = ["pequena", "média", "media", "grande"]

        if tamanho and tamanho.lower() in validos:
            # normalize accent: if 'media' -> 'média'
            tamanho_norm = "média" if tamanho.lower() in ["media", "média"] else tamanho.lower()
            dispatcher.utter_message(text=f"Ok, uma pizza {tamanho_norm}.")
            return [SlotSet("tamanho", tamanho_norm)]
        else:
            dispatcher.utter_message(text="Desculpe, não conheço esse tamanho. Temos: pequena, média e grande.")
            return [SlotSet("tamanho", None)]


class ActionAskIngrediente(Action):
    """Pergunta se o usuário quer ingrediente extra e seta o slot de contexto."""

    def name(self) -> Text:
        return "action_ask_ingrediente"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        dispatcher.utter_message(text="Deseja adicionar algum ingrediente extra? Se sim, diga qual (ex: milho). Se não, responda 'não'.")
        # seta flag para sabermos que estamos esperando resposta sobre ingrediente
        return [SlotSet("esperando_ingrediente", True)]


class ActionRegistrarIngredienteExtra(Action):
    """Registra o ingrediente extra (ou 'não') e avança para a confirmação do pedido."""

    def name(self) -> Text:
        return "action_registrar_ingrediente_extra"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        ingrediente = tracker.get_slot("ingrediente")
        sabor = tracker.get_slot("sabor") or "—"
        tamanho = tracker.get_slot("tamanho") or "—"
        borda = tracker.get_slot("borda") or "—"

        latest_intent = tracker.latest_message.get('intent', {}).get('name')
        latest_text = (tracker.latest_message.get('text') or "").strip().lower()

        # Caso o NLU já tenha extraído um ingrediente
        if ingrediente:
            dispatcher.utter_message(text=f"Ok, adicionei {ingrediente} ao pedido.")
            confirm_text = f"Seu pedido está correto? Uma pizza de {sabor} {tamanho}, borda {borda} e ingrediente extra {ingrediente}?"
            dispatcher.utter_message(text=confirm_text)
            return [SlotSet("esperando_ingrediente", False), SlotSet("ingrediente", ingrediente)]

        # Se o usuário respondeu 'não' (intent cancelar_pedido ou texto = 'não') -> sem ingrediente extra
        if latest_intent == "cancelar_pedido" or latest_text in ["não", "nao", "não.", "nao."]:
            dispatcher.utter_message(text="Certo, sem ingredientes extras.")
            confirm_text = f"Seu pedido está correto? Uma pizza de {sabor} {tamanho} e o tipo de borda é {borda}?"
            dispatcher.utter_message(text=confirm_text)
            return [SlotSet("esperando_ingrediente", False), SlotSet("ingrediente", None)]

        # Não entendeu: pede para repetir
        dispatcher.utter_message(text="Desculpe, não entendi. Se quiser um ingrediente extra, diga qual (ex: milho). Se não quiser, responda 'não'.")
        # mantemos esperando_ingrediente True para tentar novamente
        return []
