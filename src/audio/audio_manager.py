"""音效管理器：加载和播放音效"""
import os
import pygame

ASSETS_SOUND_DIR = os.path.join(
    os.path.dirname(os.path.dirname(os.path.dirname(__file__))),
    "assets", "sounds",
)


class AudioManager:
    """音效管理器：单例模式，管理游戏音效的加载和播放"""

    _instance: "AudioManager | None" = None

    def __init__(self):
        self._enabled: bool = True
        self._volume: float = 0.5
        self._sounds: dict[str, pygame.mixer.Sound] = {}
        self._initialized: bool = False

    @classmethod
    def get_instance(cls) -> "AudioManager":
        """获取单例实例"""
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance

    def init(self, enabled: bool = True, volume: float = 0.5) -> None:
        """初始化音效系统"""
        self._enabled = enabled
        self._volume = volume
        if not enabled:
            return
        try:
            pygame.mixer.init()
            self._initialized = True
            self._load_sounds()
        except pygame.error:
            self._initialized = False

    def _load_sounds(self) -> None:
        """加载所有音效文件"""
        sound_files = {
            "eat": "eat.wav",
            "die": "die.wav",
            "move": "move.wav",
            "select": "select.wav",
        }
        for name, filename in sound_files.items():
            path = os.path.join(ASSETS_SOUND_DIR, filename)
            if os.path.exists(path):
                try:
                    self._sounds[name] = pygame.mixer.Sound(path)
                    self._sounds[name].set_volume(self._volume)
                except pygame.error:
                    pass

    def play(self, sound_name: str) -> None:
        """播放指定音效"""
        if not self._enabled or not self._initialized:
            return
        sound = self._sounds.get(sound_name)
        if sound:
            sound.play()

    def set_enabled(self, enabled: bool) -> None:
        """设置音效开关"""
        self._enabled = enabled
        if not enabled and self._initialized:
            pygame.mixer.stop()

    def set_volume(self, volume: float) -> None:
        """设置音量（0.0 到 1.0）"""
        self._volume = max(0.0, min(1.0, volume))
        for sound in self._sounds.values():
            sound.set_volume(self._volume)
