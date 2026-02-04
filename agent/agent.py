import os
import json
import logging
from typing import Dict, Optional
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
                 model_name: str = "gpt-4.1",
                 temperature: float = 0.7,
                 api_key: Optional[str] = None,
                 system_prompt: Optional[str] = None):
        """
        Initialize the Agent.
        
        Args:
            model_name: OpenAI model to use (e.g., 'gpt-4', 'gpt-4o-mini')
            temperature: Sampling temperature (0.0 to 1.0)
            api_key: OpenAI API key (if None, reads from OPENAI_API_KEY env var)
        """
        self.model_name = model_name
        self.temperature = temperature
        self.api_key = api_key or os.getenv("OPENAI_API_KEY")
        self.system_prompt = system_prompt
        
        if not self.api_key:
            raise ValueError(
                "OpenAI API key not found. Set OPENAI_API_KEY environment variable "
                "or create .env file with: OPENAI_API_KEY=your_key_here"
            )
        
        self.client = OpenAI(api_key=self.api_key)
        
        logger.info(f"Agent initialized with model: {model_name}")

    def _build_messages(self, user_payload: Dict) -> list:
        messages = []
        if self.system_prompt:
            messages.append({"role": "system", "content": self.system_prompt})
        messages.append({"role": "user", "content": json.dumps(user_payload)})
        return messages

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
        messages = self._build_messages(payload)
        response = self.client.chat.completions.create(
            model=self.model_name,
            temperature=self.temperature,
            messages=messages,
        )
        content = response.choices[0].message.content or "{}"
        return self._parse_json_response(content)

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
        messages = self._build_messages(payload)
        response = self.client.chat.completions.create(
            model=self.model_name,
            temperature=self.temperature,
            messages=messages,
        )
        content = response.choices[0].message.content or "{}"
        return self._parse_json_response(content)

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
        messages = self._build_messages(payload)
        response = self.client.chat.completions.create(
            model=self.model_name,
            temperature=self.temperature,
            messages=messages,
        )
        content = response.choices[0].message.content or "{}"
        return self._parse_json_response(content)
    
    
    