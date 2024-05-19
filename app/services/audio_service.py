from typing import Sequence, Dict

from app.data.dal import AudioDAL
from app.services import SettingsService
from app.schemas import Audio


class AudioService:
    def __init__(
            self,
            audio_dal: AudioDAL,
            settings_service: SettingsService
    ) -> None:
        self.audio_dal = audio_dal
        self.settings_service = settings_service

    async def add_audio(self, audios: Sequence | Dict) -> None:
        await self.audio_dal.add(audios)

    async def get_audios(self, **kwargs) -> Sequence[Audio] | None:
        audios = await self.audio_dal.get_all(**kwargs)
        return audios
    
    async def get_audio(self, **kwargs) -> Audio:
        audio = await self.audio_dal.get_one(**kwargs)
        return audio
    
    