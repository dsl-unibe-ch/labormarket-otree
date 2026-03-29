import os
import json
import logging
from typing import Any, Dict, Optional
from pathlib import Path
import sys
from openai import OpenAI
from dotenv import load_dotenv

# Add parent directory to path to import prompt_builder
sys.path.insert(0, str(Path(__file__).parent.parent))

# Load .env from project root (agent/ is in project root)
project_root = Path(__file__).parent.parent
load_dotenv(dotenv_path=project_root / ".env")


# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
logger = logging.getLogger(__name__)


class Agent:
    """
    AI Agent that plays the labor market game using LLM.
    Uses PromptBuilder to generate prompts and makes decisions via OpenAI API.
    """
    
    def __init__(self,
                 model_name: str = "gpt-5.4",
                 api_key: Optional[str] = None,
                 system_prompt: Optional[str] = None,
                 conversation_id: Optional[str] = None):
        """
        Initialize the Agent.
        
        Args:
            model_name: OpenAI model to use (e.g., 'gpt-4', 'gpt-4o-mini')
            api_key: OpenAI API key (if None, reads from OPENAI_API_KEY env var)
        """
        self.model_name = model_name
        self.api_key = api_key or os.getenv("OPENAI_API_KEY")
        self.system_prompt = system_prompt
        self.conversation_id = conversation_id
        
        if not self.api_key:
            raise ValueError(
                "OpenAI API key not found. Set OPENAI_API_KEY environment variable "
                "or create .env file with: OPENAI_API_KEY=your_key_here"
            )
        
        self.client = OpenAI(api_key=self.api_key)
        
        logger.info(f"Agent initialized with model: {model_name}")

    def _build_input(self, user_payload: Dict) -> list[Dict[str, str]]:
        return [{"role": "user", "content": json.dumps(user_payload)}]

    def _extract_text(self, response: Any) -> str:
        text = getattr(response, "output_text", None)
        if text:
            return text
        output = getattr(response, "output", None)
        if not output:
            return "{}"
        chunks: list[str] = []
        for item in output:
            content = getattr(item, "content", None) or []
            for c in content:
                c_text = getattr(c, "text", None)
                if c_text:
                    chunks.append(c_text)
        return "\n".join(chunks) if chunks else "{}"

    def _run(self, user_payload: Dict) -> Dict:
        task = user_payload.get("task", "?")
        participant_id = user_payload.get("participant_id")
        conversation_sent = self.conversation_id

        request: Dict[str, Any] = {
            "model": self.model_name,
            "input": self._build_input(user_payload),
        }
        if self.system_prompt:
            request["instructions"] = self.system_prompt
        if self.conversation_id:
            request["conversation"] = self.conversation_id

        response = self.client.responses.create(**request)

        response_id = getattr(response, "id", None)
        next_conversation_id = (
            getattr(response, "conversation", None)
            or getattr(response, "conversation_id", None)
        )
        if next_conversation_id:
            self.conversation_id = next_conversation_id

        # Trace threading: grep logs for "OpenAI conversation trace".
        # - First call for a participant: conversation_sent=None, conversation_returned should be conv_...
        # - Later calls: conversation_sent equals that conv_... (same thread for this player).
        logger.info(
            "OpenAI conversation trace: participant_id=%s task=%s "
            "conversation_sent=%s response_id=%s conversation_returned=%s",
            participant_id,
            task,
            conversation_sent,
            response_id,
            next_conversation_id,
        )
        if not next_conversation_id:
            logger.warning(
                "OpenAI response had no conversation id (participant_id=%s task=%s response_id=%s); "
                "server-side thread may not persist for the next call.",
                participant_id,
                task,
                response_id,
            )

        content = self._extract_text(response)
        return self._parse_json_response(content)

    def _parse_json_response(self, content: str) -> Dict:
        try:
            return json.loads(content)
        except json.JSONDecodeError:
            start = content.find("{")
            end = content.rfind("}")
            if start == -1 or end == -1 or end <= start:
                raise
            return json.loads(content[start:end + 1])

    def choose_effort(self, participant_id: int, game_state: Dict) -> Dict:
        payload = {
            "task": "ChooseEffort",
            "participant_id": participant_id,
            "instruction": (
                "Choose an effort level from 1 to 10. "
                "Return JSON with keys: work_effort (int 1-10) and reasoning (string)."
            ),
            "game_state": game_state,
        }
        return self._run(payload)

    def make_offer(self, participant_id: int, game_state: Dict) -> Dict:
        payload = {
            "task": "MakeOffer",
            "participant_id": participant_id,
            "instruction": (
                "Choose an employee to offer to (or 0 for no offer). "
                "Return JSON with keys: offer_employee (int), offer_wage (int), "
                "offer_training (bool), and reasoning (string)."
            ),
            "game_state": game_state,
        }
        return self._run(payload)

    def respond_to_offer(self, participant_id: int, game_state: Dict) -> Dict:
        payload = {
            "task": "GetOffers",
            "participant_id": participant_id,
            "instruction": (
                "Choose a manager to accept (by manager id), or 0 to reject all offers. "
                "Return JSON with keys: player_matched (int) and reasoning (string)."
            ),
            "game_state": game_state,
        }
        return self._run(payload)
    
    
    