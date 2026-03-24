from app.domain.entities import AudioResult, WordEntry


def test_word_entry_fields() -> None:
    entry = WordEntry(
        word="clarity",
        phonetic="/ˈkler.ə.ti/",
        spelling="C-L-A-R-I-T-Y",
        meaning="The quality of being easy to understand.",
        example_en="Clarity matters in technical interviews.",
        example_es="La claridad importa en entrevistas técnicas.",
    )

    assert entry.word == "clarity"
    assert entry.spelling == "C-L-A-R-I-T-Y"


def test_audio_result_fields() -> None:
    entry = WordEntry("clarity", "/ˈkler.ə.ti/", "C-L-A-R-I-T-Y", "Meaning", "Example", "Ejemplo")
    result = AudioResult(word_entry=entry, audio_url="/api/audio/file.mp3", audio_filename="file.mp3", slow=False)

    assert result.audio_filename == "file.mp3"
