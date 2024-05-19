from sqlalchemy import insert, select, exists, update
from sqlalchemy.ext.asyncio import AsyncSession

from app.schemas import Audio
from app.data.models import AudioModel


class AudioDAL:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def exists(self, **kwargs) -> bool:
        query = select(exists().where(
            *(getattr(AudioModel, key) == value
              for key, value in kwargs.items()
              if hasattr(AudioModel, key))
        ))

        result = await self.session.execute(query)
        return result.scalar_one()

    async def add(self, user_audio: list | dict) -> None:
        query = insert(AudioModel).values(user_audio)
        await self.session.execute(query)
        await self.session.commit()

    async def get_one(self, **kwargs) -> Audio:
        query = select(AudioModel).filter_by(**kwargs)
        results = await self.session.execute(query)
        db_audio = results.scalar_one()

        return Audio(
            id=db_audio.id,
            user_id=db_audio.user_id,
            audio=db_audio.audio
        )

    async def get_all(self, **kwargs) -> list[Audio]:
        exists = await self.exists(**kwargs)
        
        if not exists:
            return None
        
        query = select(AudioModel).filter_by(**kwargs)
        results = await self.session.execute(query)
        db_audios = results.scalars().all()
     
        return [
            Audio(
                id=db_audio.id,
                user_id=db_audio.user_id,
                audio=db_audio.audio
            ) for db_audio in db_audios
        ]

    async def get_last_index(self, user_id: int) -> int:
        query = (
            select(AudioModel.audio_index)
            .filter_by(user_id=user_id)
            .order_by(AudioModel.audio_index.desc())
        )
        results = await self.session.execute(query)
        last_index = results.scalars().first()

        return last_index


    async def update(self, audio_list: list[dict]) -> None:
        query = update(AudioModel)
        await self.session.execute(query, audio_list)
        await self.session.commit()